import argparse
import json
import os
import subprocess
import logging

expected_group_names = [
    "data-engineering-synapse",
    "databricks-rg-adbworkspace",
    "synapseworkspace-managedrg",
    "NetworkWatcherRG"
]

expected_resources = {
    'NetworkWatcherRG': [
        {
            'resource_location': 'LOCATION',
            'resource_name': 'NetworkWatcher_LOCATION',
            'resource_type': 'Microsoft.Network/networkWatchers'}
    ],
    'data-engineering-synapse': [
        {
            'resource_location': 'LOCATION',
            'resource_name': 'asastoreSUFFIX',
            'resource_type': 'Microsoft.Storage/storageAccounts'},
        {
            'resource_location': 'LOCATION',
            'resource_name': 'eventhubSUFFIX',
            'resource_type': 'Microsoft.EventHub/namespaces'},
        {
            'resource_location': 'LOCATION',
            'resource_name': 'asadatalakeSUFFIX',
            'resource_type': 'Microsoft.Storage/storageAccounts'},
        {
            'resource_location': 'LOCATION',
            'resource_name': 'asakeyvaultSUFFIX',
            'resource_type': 'Microsoft.KeyVault/vaults'},
        {
            'resource_location': 'LOCATION',
            'resource_name': 'asaSUFFIX',
            'resource_type': 'Microsoft.StreamAnalytics/streamingjobs'},
        {
            'resource_location': 'LOCATION',
            'resource_name': 'adbworkspaceSUFFIX',
            'resource_type': 'Microsoft.Databricks/workspaces'},
        {
            'resource_location': 'LOCATION',
            'resource_name': 'asaworkspaceSUFFIX',
            'resource_type': 'Microsoft.Synapse/workspaces'},
        {
            'resource_location': 'LOCATION',
            'resource_name': 'asacosmosdbSUFFIX',
            'resource_type': 'Microsoft.DocumentDB/databaseAccounts'},
        {
            'resource_location': 'LOCATION',
            'resource_name': 'asaworkspaceSUFFIX/SparkPool01',
            'resource_type': 'Microsoft.Synapse/workspaces/bigDataPools'}
    ],
    'databricks-rg-adbworkspace': [
        {
            'resource_location': 'LOCATION',
            'resource_name': 'dbstorageRANDOMSTRING',
            'resource_type': 'Microsoft.Storage/storageAccounts'},
        {
            'resource_location': 'LOCATION',
            'resource_name': 'dbmanagedidentity',
            'resource_type': 'Microsoft.ManagedIdentity/userAssignedIdentities'},
        {
            'resource_location': 'LOCATION',
            'resource_name': 'workers-sg',
            'resource_type': 'Microsoft.Network/networkSecurityGroups'},
        {
            'resource_location': 'LOCATION',
            'resource_name': 'workers-vnet',
            'resource_type': 'Microsoft.Network/virtualNetworks'}],
    'synapseworkspace-managedrg': [
        {
            'resource_location': 'LOCATION',
            'resource_name': 'asaworkspaceSUFFIX',
            'resource_type': 'Microsoft.Sql/servers'},
        {
            'resource_location': 'LOCATION',
            'resource_name': 'asaworkspaceSUFFIX/master',
            'resource_type': 'Microsoft.Sql/servers/databases'}
    ]
}


def process_shell_command(shell_command):
    output = subprocess.getoutput(shell_command)
    try:
        result = json.loads(output)
    except json.JSONDecodeError:
        result = output
    return result


def run_test(tenant_id, user, password, path):

    logging.debug(f"Connecting as '{user}'...")
    connection_string = f"az login -t \"{tenant_id}\" -u \"{user}\" -p \"{password}\""
    connection = process_shell_command(connection_string)[0]
    logging.debug(f"Subscription found: '{connection['id']}'")
    logging.debug("Connection ok")

    logging.debug("Getting groups ...")
    groups = process_shell_command("az group list")
    if len(groups) != 4:
        raise ValueError(
            f"Number of resource groups should be 4: (got {len(groups)}"
        )
    logging.debug("Resource groups ok")
    logging.debug(f"{len(groups)} found (expected: 4)")

    logging.debug("Getting resources ...")
    resources = process_shell_command("az resource list")
    if len(resources) != 16:
        raise ValueError(
            f"Number of resources should be 16: (got {len(resources)}"
        )
    logging.debug(f"{len(resources)} found (expected: 16)")
    logging.debug("Resources ok")

    logging.debug("Getting suffix ...")
    suffix = process_shell_command(
        "az tag list --query \"[?tagName == 'DeploymentId'] | [0].values[0].tagValue\"")
    logging.debug("Suffix ok")
    logging.debug(f"Suffix is '{suffix}'")

    logging.debug("Checking Resource Group names ...")
    clean_group_names = {}
    for g in groups:
        right_name = False
        for e in expected_group_names:
            if g["name"][:len(e)] == e:
                clean_group_names[g["name"]] = e
                right_name = True
        if not right_name:
            raise ValueError(
                f"Resource group name '{g}' does not match the expected resource group names"
            )
    logging.debug("Resource groups'  names ok")

    logging.debug("Checking resources location...")
    locations = set([r["location"] for r in resources])
    if len(locations) != 1:
        raise ValueError(
            f"Location is multiple: {locations}"
        )
    else:
        location = locations.pop()
        logging.debug(f"Location is '{location}'")

    logging.debug("Checking resources ...")
    resource_group_resources = {}
    for r in resources:
        resource_group_name = r["resourceGroup"]
        resource_name = r["name"]
        if resource_name[:9] == "dbstorage":
            random_string = resource_name[9:]
            resource_name = "dbstorageRANDOMSTRING"
        resource_type = r["type"]
        resource_location = r["location"]
        resource_group_name_clean = ""
        for rgn in expected_group_names:
            if resource_group_name[:len(rgn)] == rgn:
                resource_group_name_clean = rgn

        if resource_group_name_clean not in resource_group_resources:
            resource_group_resources[resource_group_name_clean] = []

        resource_group_resources[resource_group_name_clean].append(
            {
                "resource_name": resource_name.replace(suffix, "SUFFIX").replace(location, "LOCATION"),
                "resource_type": resource_type,
                "resource_location": resource_location.replace(location, "LOCATION")
            }
        )

    if resource_group_resources != expected_resources:
        raise ValueError(
            "Resources are different that expected"
        )
    logging.debug("Resources ok")

    logging.debug("Checking Data Lake content ...")
    local_files = get_local_filenames(path=path)
    remote_files = get_filenames_from_datalake(suffix=suffix)
    remote_minus_local = remote_files.difference(local_files)
    local_minus_remote = local_files.difference(remote_files)
    if len(remote_minus_local) != 0:
        raise ValueError(
            f"Some files in the data lake are not in local repo: \n{remote_minus_local}"
        )
    if local_minus_remote != {'sale-csv', 'sale-csv/deleteme.txt'}:
        raise ValueError(
            f"Remote files missing: \n {local_minus_remote}"
        )
    logging.debug("Data Lake content ok")


def get_local_filenames(path):

    local_files = []

    for root, folders, files in os.walk(top=path):
        local_files.extend(
            [
                os.path.join(root, f).split("wwi-02/", 1)[1] for f in files
            ]
        )
        local_files.extend(
            [
                os.path.join(root, f).split("wwi-02/", 1)[1] for f in folders
            ]
        )
    local_files = set(local_files)
    return local_files


def get_filenames_from_datalake(suffix):
    logging.debug(f"Getting blob info from asadatalake{suffix}")
    blobs = process_shell_command(
        f"az storage blob list  --account-name asadatalake{suffix}  --container-name wwi-02 --num-results '*' --auth-mode login")
    blobs = json.loads(blobs.split("\n", 2)[-1])
    file_names = set([b["name"] for b in blobs])
    logging.debug(f"Received {len(file_names)} files")

    return file_names


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "--tenant_id", "-t",
        help="ID of the tenant (can be found in Azure Active Directory)",
        default="3670fdab-17f6-4743-b8f8-6ac0784204aa"
    )
    argument_parser.add_argument(
        "--user", "-u",
        help="Username (email of the user)",
        default="pauldechorgnat@dp203sept.onmicrosoft.com",
    )
    argument_parser.add_argument(
        "--password", "-p",
        help="Password of the account",
        default="DataScientest123!"
    )
    argument_parser.add_argument(
        "--debug", "-d",
        help="Debug mode",
        action="store_true"
    )

    argument_parser.add_argument(
        "--path",
        help="Path to wwi-02 local folder",
        default="/home/paul/Desktop/00_DataScientest/DP-203-Data-Engineer/Allfiles/wwi-02/"
    )

    arguments = argument_parser.parse_args()
    tenant_id = arguments.tenant_id
    user = arguments.user
    password = arguments.password
    debug_mode = arguments.debug
    path_to_wwi_02 = arguments.path

    if debug_mode:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s,%(msecs)d %(levelname)-8s [%(pathname)s:%(lineno)d (%(funcName)s()] %(process)d:"
            " %(message)s",
            datefmt="%d-%m-%Y:%H:%M:%S",
        )

    run_test(tenant_id, user, password, path=path_to_wwi_02)

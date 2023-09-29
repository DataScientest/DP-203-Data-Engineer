# Definition des parametres
$tenantId = "3670fdab-17f6-4743-b8f8-6ac0784204aa"

$user = $args[0]
$password = $args[1]


# Sécurisation des mots de passe
$securePassword = $password | ConvertTo-SecureString -AsPlainText -Force
$credentials = New-Object -TypeName "System.Management.Automation.PSCredential" -ArgumentList $user,$securePassword

# Connexion a Azure
$subscription = (az login -t $tenantId -u $user -p $password | ConvertFrom-JSON)[0]

$subscriptionId = ($subscription).id


# Récupération des Resources Groupes
$groups = (az group list | ConvertFrom-JSON) 

$uniqueSuffix = az tag list --query "[?tagName == 'DeploymentId'] | [0].values[0].tagValue"

# $resourceGroupNames = [
#     "data-engineering-synapse-" + $uniqueSuffix,
#     "databricks-rg-adbworkspace" + $uniqueSuffix + "-",
#     "synapseworkspace-managedrg-",
#     "NetworkWatcherRG"
# ]

$resourceGroups = (az group list | ConvertFrom-JSON)

for ($i =0; $i -le ($resourceGroups).length; $i += 1) {
    Write-Host ($resourceGroups)[$i].location
}


# ($resourceGroupNames).GetType()
# $locations

# $resourceGroupContent = {
#     "NetworkWatcherRG": [
#         {
#             "type": "Microsoft.Network/networkWatchers",
#             "name": "NetworkWatcher_" + $location
#         }
#     ]
# }



# On doit avoir 4 groupes de ressource
Write-Host ($groups).length
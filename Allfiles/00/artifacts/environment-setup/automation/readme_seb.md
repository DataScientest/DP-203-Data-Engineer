# Documentation des différentes opérations de déploiement

1. Commande de déploiement:

**Exemple de commande:**
``` powershell
pwsh ./dp-203-setup.ps1 3670fdab-17f6-4743-b8f8-6ac0784204aa sebastien.s@dp203sept.onmicrosoft.com Rudu39081
```

* `3670fdab-17f6-4743-b8f8-6ac0784204aa` : est le tenat ID
* `sebastien.s@dp203sept.onmicrosoft.com` : mail de l'apprenant
* `Rudu39081` : MDP de l'apprenant

## Step 1: Création d'un fichier CSV

* Tenant ID: 79b1cadf-573c-4d97-95d0-00fb5675ff07

### Création des ressources

``` powershell
# Abdal OK
pwsh ./dp-203-setup.ps1 79b1cadf-573c-4d97-95d0-00fb5675ff07 abdellatif.aazmi@dp203nov.onmicrosoft.com Rh9ZjZx7E9n6
# Naht OK
pwsh ./dp-203-setup.ps1 79b1cadf-573c-4d97-95d0-00fb5675ff07 nhat.dao@dp203nov.onmicrosoft.com T8iL7iq6M6aM
# Aysha OK
pwsh ./dp-203-setup.ps1 79b1cadf-573c-4d97-95d0-00fb5675ff07 aysha.kadaikar@dp203nov.onmicrosoft.com fVmR26LJ32bk
# tawfik OK
pwsh ./dp-203-setup.ps1 79b1cadf-573c-4d97-95d0-00fb5675ff07 tawfik.borji@dp203nov.onmicrosoft.com Mc8JGN4hg44g
# marylis OK
pwsh ./dp-203-setup.ps1 79b1cadf-573c-4d97-95d0-00fb5675ff07 marylis.rubrice@dp203nov.onmicrosoft.com 3m6VK2vNWg4e

# saber NO OK (westeurope ???) --> eastasia A FAIRE
pwsh ./dp-203-setup.ps1 79b1cadf-573c-4d97-95d0-00fb5675ff07 saber.zribi@dp203nov.onmicrosoft.com T7jkaBgDX328

# ameni en cours
pwsh ./dp-203-setup.ps1 79b1cadf-573c-4d97-95d0-00fb5675ff07 ameni.chebbi@dp203nov.onmicrosoft.com u2d99F7dzCLL

# hamid A faire
pwsh ./dp-203-setup.ps1 79b1cadf-573c-4d97-95d0-00fb5675ff07 hamid.oukka@dp203nov.onmicrosoft.com G8v7q2Q5UdAd

# yannick A faire
pwsh ./dp-203-setup.ps1 79b1cadf-573c-4d97-95d0-00fb5675ff07 yannick.koblan@dp203nov.onmicrosoft.com VD3c8G7Aqe6y

# basile A faire
pwsh ./dp-203-setup.ps1 79b1cadf-573c-4d97-95d0-00fb5675ff07 basile.labat@dp203nov.onmicrosoft.com TeY7Zvq2qL89

# jeanarnaud A faire
pwsh ./dp-203-setup.ps1 79b1cadf-573c-4d97-95d0-00fb5675ff07 jeanarnaud.bayiha@dp203nov.onmicrosoft.com 66s3tTd3ReAT

# aymarlebondza A faire
pwsh ./dp-203-setup.ps1 79b1cadf-573c-4d97-95d0-00fb5675ff07 aymarlebondza@dp203nov.onmicrosoft.com 2P6Tbq3xZF6r

# lucverger A faire
pwsh ./dp-203-setup.ps1 79b1cadf-573c-4d97-95d0-00fb5675ff07 lucverger@dp203nov.onmicrosoft.com Lvb63wY53dJY

# pierregroshens A faire
pwsh ./dp-203-setup.ps1 79b1cadf-573c-4d97-95d0-00fb5675ff07 pierregroshens@dp203nov.onmicrosoft.com NGj5z9U88fnS
```


## Réalisation des tests
```shell
cd ../tests
python3 test.py -d -t 79b1cadf-573c-4d97-95d0-00fb5675ff07 -u abdellatif.aazmi@dp203nov.onmicrosoft.com -p Rh9ZjZx7E9n6 --path /dp-203/DP-203-Data-Engineer/Allfiles/wwi-02
```
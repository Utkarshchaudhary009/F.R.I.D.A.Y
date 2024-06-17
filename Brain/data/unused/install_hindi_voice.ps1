# PowerShell script to install Hindi language pack
Add-WindowsCapability -Online -Name Language.Basic~~~hi-IN~0.0.1.0
Add-WindowsCapability -Online -Name Language.Handwriting~~~hi-IN~0.0.1.0
Add-WindowsCapability -Online -Name Language.Speech~~~hi-IN~0.0.1.0
Add-WindowsCapability -Online -Name Language.TextToSpeech~~~hi-IN~0.0.1.0

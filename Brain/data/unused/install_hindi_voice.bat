@echo off
:: Batch script to run PowerShell script with elevated privileges
PowerShell -Command "Start-Process PowerShell -ArgumentList 'Set-ExecutionPolicy RemoteSigned -Scope Process; ./install_hindi_voice.ps1' -Verb RunAs"

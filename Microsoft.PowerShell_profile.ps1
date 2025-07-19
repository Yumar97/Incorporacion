# Configuración permanente de Python 3.12
$env:PATH = "C:\Users\yumar\AppData\Local\Programs\Python\Python312\Scripts\;C:\Users\yumar\AppData\Local\Programs\Python\Python312\;" + $env:PATH

# Alias para asegurar que python siempre use la versión correcta
Set-Alias -Name python -Value "C:\Users\yumar\AppData\Local\Programs\Python\Python312\python.exe" -Force

Write-Host "✅ Python 3.12 configurado automáticamente" -ForegroundColor Green
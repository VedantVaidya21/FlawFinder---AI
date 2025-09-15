# Fix dark-* classes to use zinc colors
$files = Get-ChildItem -Path "C:\Users\vedan\flawfinder-ai\src" -Recurse -Filter "*.jsx"

foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw
    
    # Replace dark-* classes with zinc equivalents
    $content = $content -replace "bg-dark-50", "bg-zinc-900"
    $content = $content -replace "bg-dark-100", "bg-zinc-800"
    $content = $content -replace "bg-dark-200", "bg-zinc-700"
    $content = $content -replace "bg-dark-300", "bg-zinc-600"
    $content = $content -replace "bg-dark-400", "bg-zinc-500"
    $content = $content -replace "bg-dark-500", "bg-zinc-400"
    $content = $content -replace "bg-dark-600", "bg-zinc-300"
    $content = $content -replace "bg-dark-700", "bg-zinc-200"
    $content = $content -replace "bg-dark-800", "bg-zinc-100"
    $content = $content -replace "bg-dark-900", "bg-zinc-50"
    
    $content = $content -replace "text-dark-50", "text-zinc-900"
    $content = $content -replace "text-dark-100", "text-zinc-800"
    $content = $content -replace "text-dark-200", "text-zinc-700"
    $content = $content -replace "text-dark-300", "text-zinc-600"
    $content = $content -replace "text-dark-400", "text-zinc-500"
    $content = $content -replace "text-dark-500", "text-zinc-400"
    $content = $content -replace "text-dark-600", "text-zinc-300"
    $content = $content -replace "text-dark-700", "text-zinc-200"
    $content = $content -replace "text-dark-800", "text-zinc-100"
    $content = $content -replace "text-dark-900", "text-zinc-50"
    
    $content = $content -replace "border-dark-50", "border-zinc-900"
    $content = $content -replace "border-dark-100", "border-zinc-800"
    $content = $content -replace "border-dark-200", "border-zinc-700"
    $content = $content -replace "border-dark-300", "border-zinc-600"
    $content = $content -replace "border-dark-400", "border-zinc-500"
    $content = $content -replace "border-dark-500", "border-zinc-400"
    $content = $content -replace "border-dark-600", "border-zinc-300"
    $content = $content -replace "border-dark-700", "border-zinc-200"
    $content = $content -replace "border-dark-800", "border-zinc-100"
    $content = $content -replace "border-dark-900", "border-zinc-50"
    
    $content = $content -replace "hover:bg-dark-50", "hover:bg-zinc-900"
    $content = $content -replace "hover:bg-dark-100", "hover:bg-zinc-800"
    $content = $content -replace "hover:bg-dark-200", "hover:bg-zinc-700"
    $content = $content -replace "hover:bg-dark-300", "hover:bg-zinc-600"
    $content = $content -replace "hover:bg-dark-400", "hover:bg-zinc-500"
    $content = $content -replace "hover:bg-dark-500", "hover:bg-zinc-400"
    $content = $content -replace "hover:bg-dark-600", "hover:bg-zinc-300"
    $content = $content -replace "hover:bg-dark-700", "hover:bg-zinc-200"
    $content = $content -replace "hover:bg-dark-800", "hover:bg-zinc-100"
    $content = $content -replace "hover:bg-dark-900", "hover:bg-zinc-50"
    
    $content = $content -replace "hover:text-dark-50", "hover:text-zinc-900"
    $content = $content -replace "hover:text-dark-100", "hover:text-zinc-800"
    $content = $content -replace "hover:text-dark-200", "hover:text-zinc-700"
    $content = $content -replace "hover:text-dark-300", "hover:text-zinc-600"
    $content = $content -replace "hover:text-dark-400", "hover:text-zinc-500"
    $content = $content -replace "hover:text-dark-500", "hover:text-zinc-400"
    $content = $content -replace "hover:text-dark-600", "hover:text-zinc-300"
    $content = $content -replace "hover:text-dark-700", "hover:text-zinc-200"
    $content = $content -replace "hover:text-dark-800", "hover:text-zinc-100"
    $content = $content -replace "hover:text-dark-900", "hover:text-zinc-50"
    
    $content = $content -replace "hover:border-dark-50", "hover:border-zinc-900"
    $content = $content -replace "hover:border-dark-100", "hover:border-zinc-800"
    $content = $content -replace "hover:border-dark-200", "hover:border-zinc-700"
    $content = $content -replace "hover:border-dark-300", "hover:border-zinc-600"
    $content = $content -replace "hover:border-dark-400", "hover:border-zinc-500"
    $content = $content -replace "hover:border-dark-500", "hover:border-zinc-400"
    $content = $content -replace "hover:border-dark-600", "hover:border-zinc-300"
    $content = $content -replace "hover:border-dark-700", "hover:border-zinc-200"
    $content = $content -replace "hover:border-dark-800", "hover:border-zinc-100"
    $content = $content -replace "hover:border-dark-900", "hover:border-zinc-50"
    
    # Fix some specific inversions for better contrast
    $content = $content -replace "text-zinc-50", "text-zinc-100"
    $content = $content -replace "text-zinc-900", "text-zinc-400"
    
    Set-Content -Path $file.FullName -Value $content
}

Write-Host "Fixed all dark-* classes to use zinc colors"

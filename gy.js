document.getElementById('downloadBtn').addEventListener('click', () => {
    const symptoms = document.getElementById('symptoms').value;
    const hr = document.getElementById('hr').value;
    const temp = document.getElementById('temp').value;
    const bp = document.getElementById('bp').value;

    let reportText = `MEDICAL REPORT\nDate: ${new Date().toLocaleString()}\n`;
    reportText += `==============================\n`;
    reportText += `Vitals: HR ${hr}, Temp ${temp}, BP ${bp}\n`;
    reportText += `Symptoms: ${symptoms}\n`;
    
    // Create a virtual file and download it
    const blob = new Blob([reportText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Report_${Date.now()}.txt`;
    a.click();
});
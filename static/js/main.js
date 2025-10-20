document.addEventListener('DOMContentLoaded', () => {
    const stateSel = document.getElementById('state');
    const districtSel = document.getElementById('district');
    const complexSel = document.getElementById('complex');
    const courtSel = document.getElementById('court');
    const dateInput = document.getElementById('date');
    const listType = document.getElementById('listType');
    const form = document.getElementById('scrapeForm');
    const resultDiv = document.getElementById('result');

    async function fetchStates(){
        stateSel.innerHTML = '<option value="">Loading...</option>';
        const res = await fetch('/api/states');
        const j = await res.json();
        if(j.success){
            stateSel.innerHTML = '<option value="">Select State</option>';
            j.data.forEach(s => {
                const o = document.createElement('option');
                o.value = s.value; o.text = s.text;
                stateSel.appendChild(o);
            });
        } else {
            stateSel.innerHTML = '<option value="">Failed to load</option>';
        }
    }

    async function fetchDistricts(stateCode){
        districtSel.innerHTML = '<option value="">Loading...</option>';
        const res = await fetch(`/api/districts/${stateCode}`);
        const j = await res.json();
        if(j.success){
            districtSel.innerHTML = '<option value="">Select District</option>';
            j.data.forEach(d => {
                const o = document.createElement('option');
                o.value = d.value; o.text = d.text;
                districtSel.appendChild(o);
            });
            districtSel.disabled = false;
        } else {
            districtSel.innerHTML = '<option value="">Failed to load</option>';
        }
    }

    async function fetchComplexes(){
        complexSel.innerHTML = '<option value="">Loading...</option>';
        const st = stateSel.value, dt = districtSel.value;
        const res = await fetch(`/api/complexes/${st}/${dt}`);
        const j = await res.json();
        if(j.success){
            complexSel.innerHTML = '<option value="">Select Complex</option>';
            j.data.forEach(c => {
                const o = document.createElement('option');
                o.value = c.value; o.text = c.text;
                complexSel.appendChild(o);
            });
            complexSel.disabled = false;
        } else {
            complexSel.innerHTML = '<option value="">Failed to load</option>';
        }
    }

    async function fetchCourts(){
        courtSel.innerHTML = '<option value="">Loading...</option>';
        const st = stateSel.value, dt = districtSel.value, cp = complexSel.value;
        const res = await fetch(`/api/courts/${st}/${dt}/${cp}`);
        const j = await res.json();
        if(j.success){
            courtSel.innerHTML = '<option value="">Select Court</option>';
            j.data.forEach(c => {
                const o = document.createElement('option');
                o.value = c.value; o.text = c.text;
                courtSel.appendChild(o);
            });
            courtSel.disabled = false;
        } else {
            courtSel.innerHTML = '<option value="">Failed to load</option>';
        }
    }

    stateSel.addEventListener('change', (e) => {
        const val = e.target.value;
        districtSel.disabled = true; complexSel.disabled = true; courtSel.disabled = true;
        districtSel.innerHTML = '<option value="">Select State first</option>';
        complexSel.innerHTML = '<option value="">Select District first</option>';
        courtSel.innerHTML = '<option value="">Select Complex first</option>';
        if(val) fetchDistricts(val);
    });

    districtSel.addEventListener('change', (e) => {
        complexSel.disabled = true; courtSel.disabled = true;
        complexSel.innerHTML = '<option value="">Select District first</option>';
        courtSel.innerHTML = '<option value="">Select Complex first</option>';
        if(districtSel.value) fetchComplexes();
    });

    complexSel.addEventListener('change', (e) => {
        courtSel.disabled = true;
        courtSel.innerHTML = '<option value="">Select Complex first</option>';
        if(complexSel.value) fetchCourts();
    });

    form.addEventListener('submit', async (ev) => {
        ev.preventDefault();
        resultDiv.innerHTML = 'Processing... this may take a while if live scraping is used.';
        const payload = {
            state: stateSel.value,
            district: districtSel.value,
            complex: complexSel.value,
            court: courtSel.value,
            date: dateInput.value,
            listType: listType.value
        };
        const res = await fetch('/api/scrape', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(payload)
        });
        const j = await res.json();
        if(j.success){
            resultDiv.innerHTML = '<a id="downloadLink" href="/download/' + j.filename + '">Download PDF</a>';
            window.location = '/download/' + j.filename;
        } else {
            resultDiv.innerText = 'Error: ' + (j.error || 'Unknown error');
        }
    });

    fetchStates();
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;
});

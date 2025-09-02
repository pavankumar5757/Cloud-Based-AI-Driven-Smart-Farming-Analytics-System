 async function postJSON(url, data) {
   const res = await fetch(url, {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify(data)
   });
   return res.json();
 }

 function serializeForm(form) {
   const data = {};
   new FormData(form).forEach((v, k) => { data[k] = v; });
   return data;
 }

 document.addEventListener('DOMContentLoaded', () => {
   const cropForm = document.getElementById('cropYieldForm');
   if (cropForm) {
     cropForm.addEventListener('submit', async (e) => {
       e.preventDefault();
       const payload = serializeForm(cropForm);
       payload.temperature = parseFloat(payload.temperature);
       payload.humidity = parseFloat(payload.humidity);
       payload.rainfall = parseFloat(payload.rainfall);
       payload.fertilizer_amount = parseFloat(payload.fertilizer_amount);
       payload.irrigation_frequency = parseFloat(payload.irrigation_frequency);
       const result = await postJSON('/api/predict/crop-yield', payload);
       const el = document.getElementById('cropYieldResult');
       el.innerHTML = `<div class="alert alert-success">Predicted yield: <strong>${result.predicted_yield}</strong> t/ha (confidence ${Math.round(result.confidence_score*100)}%)<br/>${(result.recommendations||[]).join('<br/>')}</div>`;
       if (result.predicted_yield) {
         drawCropYieldCharts(result, payload);
       }
     });
   }

   const soilForm = document.getElementById('soilHealthForm');
   if (soilForm) {
     soilForm.addEventListener('submit', async (e) => {
       e.preventDefault();
       const payload = serializeForm(soilForm);
       ['pH','nitrogen','phosphorus','potassium','organic_matter','moisture'].forEach(k=>payload[k]=parseFloat(payload[k]));
       const result = await postJSON('/api/analyze/soil-health', payload);
       const el = document.getElementById('soilHealthResult');
       el.innerHTML = `<div class="alert alert-primary">Health score: <strong>${result.health_score}</strong> / 100<br/>Status: ${result.nutrient_status}<br/>${(result.fertilizer_recommendations||[]).join('<br/>')}</div>`;
       drawSoilCharts(result, payload);
     });
   }

   const pestForm = document.getElementById('pestDetectionForm');
   if (pestForm) {
     pestForm.addEventListener('submit', async (e) => {
       e.preventDefault();
       const formData = new FormData(pestForm);
       const res = await fetch('/api/detect/pest', { method: 'POST', body: formData });
       const result = await res.json();
       const el = document.getElementById('pestDetectionResult');
       el.innerHTML = `<div class="alert alert-danger">Detected: <strong>${result.predicted_class}</strong><br/>Pest prob: ${Math.round(result.pest_probability*100)}%<br/>Disease risk: ${Math.round(result.disease_risk*100)}%<br/>${(result.treatment_recommendations||[]).join('<br/>')}</div>`;
       drawPestCharts(result);
     });
   }

   const priceForm = document.getElementById('marketPriceForm');
   if (priceForm) {
     priceForm.addEventListener('submit', async (e) => {
       e.preventDefault();
       const payload = serializeForm(priceForm);
       try { payload.historical_data = JSON.parse(payload.historical_data || '[]'); } catch { payload.historical_data = []; }
       const result = await postJSON('/api/forecast/market-price', payload);
       const el = document.getElementById('marketPriceResult');
       el.innerHTML = `<div class="alert alert-warning">Forecast generated for next 12 months.</div>`;
       drawMarketCharts(result);
     });
   }
 });

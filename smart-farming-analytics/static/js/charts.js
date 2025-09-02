 function drawCropYieldCharts(result, inputs) {
   const x = ['Temp','Humidity','Rainfall','Fertilizer','Irrigation'];
   const y = [inputs.temperature, inputs.humidity, inputs.rainfall, inputs.fertilizer_amount, inputs.irrigation_frequency];
   Plotly.newPlot('cropYieldCharts', [{x, y, type:'bar', marker:{color:'#2e7d32'}}], {title:'Factors'});
 }

 function drawSoilCharts(result, inputs) {
   const categories = ['pH','N','P','K','OM','Moisture'];
   const values = [inputs.pH, inputs.nitrogen, inputs.phosphorus, inputs.potassium, inputs.organic_matter, inputs.moisture];
   const data = [{type:'scatterpolar', r:values, theta:categories, fill:'toself', name:'Soil'}];
   Plotly.newPlot('soilHealthCharts', data, {polar:{radialaxis:{visible:true, range:[0, Math.max(...values)*1.2]}}, showlegend:false, title:'Nutrient Radar'});
 }

 function drawPestCharts(result) {
   const data = [{values:[1-result.pest_probability-result.disease_risk, result.pest_probability, result.disease_risk], labels:['Healthy','Pest','Disease'], type:'pie'}];
   Plotly.newPlot('pestDetectionCharts', data, {title:'Risk Assessment'});
 }

 function drawMarketCharts(result) {
   const data = [{x: result.labels, y: result.predicted_prices, type:'scatter', mode:'lines+markers', line:{color:'#1565c0'}}];
   Plotly.newPlot('marketPriceCharts', data, {title:'Price Trend (Next 12 months)'});
 }

> **DISCLAIMER:**
-----------
> This code is provided "as-is" without any warranties or guarantees.
 The author is not responsible for the results you obtain by using it. 
Please ensure you understand the code before using it in critical applications.
If you have any questions or need clarification, you can reach out via email 
at abdelhaq.fste@gmail.com or contact me using my Slack handle: https://sanjosechapte-jto9479.slack.com/archives/D07T2ATT0P5

 > Use at your own risk.<br>

 > Author: Abdelhaq KHARROU<br>

## The Steps of the HEI Scoring Algorithm (For 2 Years and Older)
```
    # To reproduce the results within this notebooks, you could fork the env using the yml
    
    # 1 - Create env with the same dependencies using yaml config file
    conda env create -f nhanes.yml
    # Activate nhanes env
    conda activate nhanes
    # Launch jupyter-lab and enjoy
    jupyter-lab
    </code>
```

<h2> 1) Merging Files, Deriving sums</h2>
<ol>
    <li>
        <strong>Merging Files:</strong> Combine the 
        <a href="https://www.ars.usda.gov/northeast-area/beltsville-md-bhnrc/beltsville-human-nutrition-research-center/food-surveys-research-group/docs/fped-databases" target="_blank" rel="noopener noreferrer">FPED database 2017-2020 (prepandemic)</a> 
        with one of the individual foods files: 
        <a href="https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Dietary&Cycle=2017-2020" target="_blank" rel="noopener noreferrer">Dietary Interview - Individual Foods, First Day</a> 
        or 
        <a href="https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Dietary&Cycle=2017-2020" target="_blank" rel="noopener noreferrer">Dietary Interview - Individual Foods, Second Day</a>. 
        The merge is based on <code style="padding: 5px;">DRIFDCD</code> (USDA food code from IFF files) and <code style="padding: 5px;">FOODCOE</code> (FPED database). 
        Required variables include: 
        <code style="padding: 5px;">SEQN</code>, <code style="padding: 5px;">DRIFDCD</code>, <code style="padding: 5px;">DRIKCAL</code>, <code style="padding: 5px;">DRISODI</code>, <code style="padding: 5px;">DRISFAT</code>, <code style="padding: 5px;">DRIMFAT</code>, and <code style="padding: 5px;">DRIPFAT</code>. 
        These variables are calculated using the 
        <a href="https://www.ars.usda.gov/northeast-area/beltsville-md-bhnrc/beltsville-human-nutrition-research-center/food-surveys-research-group/docs/fndds-download-databases/" target="_blank" rel="noopener noreferrer">FNDDS database 2017-2018 and 2019-2020</a>, 
        as prepandemic FNDDS is not available.
    </li>
    <li>
        <strong>Aggregating Data:</strong> For each merged file, sum up the columns for each sample person to retain only one sequence number (<code style="padding: 5px;">SEQN</code>) per individual.
    </li>
    <li>
        <strong>Deriving Sums:</strong> For each HEI component, dietary constituents are summed together. For example, "Greens and Beans" is created from the sum of dark green vegetables and legumes (beans and peas). Before calculating ratios, construct variables using the following rules:
        <ol style="list-style-type: none; padding-left: 20px;">
            <li style="margin-bottom:5px;">1. <code style="padding: 5px; background:#f0f8ff"">FWHOLEFRT = F_CITMLB + F_OTHER; (FPED)</code></li>
            <li style="margin-bottom:5px;">2. <code style="padding: 5px; background:#f0f8ff">MONOPOLY = MFAT + PFAT; (FPED)</code></li>
            <li style="margin-bottom:5px;">3. <code style="padding: 5px;background:#f0f8ff"">VTOTALLEG = V_TOTAL + V_LEGUMES; (FPED)</code></li>
            <li style="margin-bottom:5px;">4. <code style="padding: 5px; background:#f0f8ff"">VDRKGRLEG = V_DRKGR + V_LEGUMES; (FPED)</code></li>
            <li style="margin-bottom:5px;">5. <code style="padding: 5px; background:#f0f8ff"">PFALLPROTLEG = PF_MPS_TOTAL + PF_EGGS + PF_NUTSDS + PF_SOY + PF_LEGUMES; (FPED)</code></li>
            <li style="margin-bottom:5px;">6. <code style="padding: 5px; background:#f0f8ff"">PFSEAPLANTLEG = PF_SEAFD_HI + PF_SEAFD_LOW + PF_NUTSDS + PF_SOY + PF_LEGUMES; (FPED)</code></li>
            <li style="margin-bottom:5px;">7. <code style="padding: 5px; background:#f0f8ff"">F_TOTAL (FPED)</code></li>
            <li style="margin-bottom:5px;">8. <code style="padding: 5px; background:#f0f8ff"">G_WHOLE (FPED)</code></li>
            <li style="margin-bottom:5px;">9. <code style="padding: 5px; background:#f0f8ff"">D_TOTAL (FPED)</code></li>
            <li style="margin-bottom:5px;">10. <code style="padding: 5px; background:#f0f8ff"">DRISFAT (P_DR1IFF and P_DR2IFF)</code></li>
            <li style="margin-bottom:5px;">11. <code style="padding: 5px; background:#f0f8ff"">DRIMFAT (P_DR1IFF and P_DR2IFF)</code></li>
            <li style="margin-bottom:5px;">12. <code style="padding: 5px; background:#f0f8ff"">DRIPFAT (P_DR1IFF and P_DR2IFF)</code></li>
            <li style="margin-bottom:5px;">13. <code style="padding: 5px; background:#f0f8ff"">DRISODI (P_DR1IFF and P_DR2IFF)</code></li>
            <li style="margin-bottom:5px;">14. <code style="padding: 5px; background:#f0f8ff"">DRIKCAL (P_DR1IFF and P_DR2IFF)</code></li>
            <li style="margin-bottom:5px;">15. <code style="padding: 5px; background:#f0f8ff"">G_REFINED (FPED)</code></li>
            <li style="margin-bottom:5px;">16. <code style="padding: 5px;background:#f0f8ff"">ADD_SUGARS (FPED)</code></li>
        </ol>
    </li>
</ol>
<p> From the table below <sup><a href="https://epi.grants.cancer.gov/hei/calculating-hei-scores.html">1</a></sup>, constructed the formulas above</p>
<table class="table table-bordered table-sm bg-white mb-3">
			<thead class="thead-dark">
				<tr>
					<th scope="col">HEI Component</th>
					<th scope="col">Dietary Constituents</th>
					<th scope="col">Additional Information</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<th colspan="3" scope="rowgroup" align="left" class="bg-lightgray">From FPED (or other food-based database)</th>
				</tr>
				<tr>
					<th align="left" scope="row">Total Fruits</th>
					<td>Total Fruits in cup equivalents</td>
					<td>Includes whole fruits and fruit juice.</td>
				</tr>
				<tr>
					<th align="left" scope="row">Whole Fruits</th>
					<td>Citrus, Melons, Berries + Other Intact Fruits in cup equivalents</td>
					<td>Excludes fruit juice.</td>
				</tr>
				<tr>
					<th align="left" scope="row">Total Vegetables</th>
					<td>Total Vegetables + Legumes (Beans and Peas) in cup equivalents</td>
					<td>&nbsp;</td>
				</tr>
				<tr>
					<th align="left" scope="row">Greens and Beans</th>
					<td> Dark Green Vegetables + Legumes (Beans and Peas) in cup equivalents</td>
					<td>&nbsp;</td>
				</tr>
				<tr>
					<th align="left" scope="row">Whole Grains</th>
					<td>Whole Grains in ounce equivalents</td>
					<td>&nbsp;</td>
				</tr>
				<tr>
				  <th align="left" scope="row">Dairy</th>
				  <td>Total Dairy in cup equivalents</td>
				  <td>Includes all milk products (e.g., fluid milk, yogurt, and cheese). Includes fortified soy milk. Excludes other plant-based milks.</td>
			  </tr>
				<tr>
				  <th align="left" scope="row">Total Protein Foods</th>
				  <td>Total Meat, Poultry, and Seafood (including organ meats and cured meats) + Eggs + Nuts and Seeds + Soy + Legumes (Beans and Peas) in ounce equivalents</td>
				  <td>Excludes fortified soy milk (which is included in Dairy). Does not include protein from all sources (e.g., does not include protein from dairy); rather, this component includes foods considered to be part of the food group Protein Foods. Lean faction only (saturated/solid fats are counted separately).</td>
			  </tr>
				<tr>
				  <th align="left" scope="row">Seafood and Plant Proteins</th>
				  <td>Seafood (high in omega-3) + Seafood (low in omega-3) + Soy + Nuts and Seeds + Legumes (Beans and Peas) in ounce equivalents</td>
				  <td>Excludes fortified soy milk (which is included in Dairy). </td>
			  </tr>
				<tr>
				  <th align="left" scope="row">Refined Grains</th>
				  <td>Refined Grains in ounce equivalents</td>
				  <td></td>
			  </tr>
				<tr>
				  <th align="left" scope="row">Added Sugars</th>
				  <td>Added Sugars</td>
				  <td>Includes caloric sweeteners and syrups used as sweeteners in other food products, and sugar added in food preparation, processing, and at the table. Teaspoon equivalents are converted to energy (kcal) in the scoring process.</td>
			  </tr>
				<tr>
					<th colspan="3" scope="rowgroup" align="left" class="bg-lightgray">From FNDDS (or other nutrient database)</th>
				</tr>
				<tr>
					<th align="left" scope="row">Energy</th>
					<td>Energy (kilocalories)</td>
					<td>Energy from foods and drinks, including alcohol. Does not include energy from supplements or nutritional supplement beverages or formulas. Does not include energy from human milk or infant/toddler formula.</td>
				</tr>
				<tr>
				  <th align="left" scope="row">Sodium</th>
				  <td>Sodium</td>
				  <td>Sodium is converted from milligrams to grams in scoring process.</td>
			  </tr>
				<tr>
				  <th align="left" scope="row">Saturated Fats</th>
				  <td>Total Saturated Fatty Acids</td>
				  <td>Saturated fats are calculated in grams but converted to energy (kcal) in the scoring process.</td>
			  </tr>
				<tr>
				  <th align="left" scope="row">Fatty Acids</th>
				  <td>(Total Monounsaturated Fatty Acids + Total Polyunsaturated Fatty Acids)/Total Saturated Fatty Acids</td>
				  <td>Calculated as a ratio. </td>
			  </tr>
			</tbody>
		</table>
<h2>2) Densities calculations and scoring</h2>
<p>
   Using the following table <sup style="font-size:14px"><a href="https://epi.grants.cancer.gov/hei/hei-2020-table1.html">2</a></sup>of adequacy, moderation components and standards for scoring(For 2 Years and Older):
</p>
    <h3>calculate HEI density ratios to be used in scoring. These categories have a density ratio per 1000 kcal.</h3>
        <h4>1) renaming variables</h4>
        <ul>
         <li style="margin-bottom:5px;"> <code style="padding:5px;background:#F0E0F0">SEQN into sequence_number</code></li>
         <li style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">DRIFDCD into food_code</code></li>
         <li style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">DRISODI into sodium_mg, then convert to sodium_g (sodium)</code></li>
         <li style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">DRIKCAL into energy_kcal</code></li>
         <li style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">DRISFAT into saturated_fats_g</code></li>
         <li style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">DRIMFAT into monounsaturated_fats_g</code></li>
         <li style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">DRIPFAT into polyunsaturated_fats_g</code></li>
         <li style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">F_TOTAL (cup eq) into total_fruits_cup</code></li>
         <li style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">G_WHOLE (oz eq) into whole_grains_oz</code></li>
         <li  style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">G_REFINED (oz eq) into refined_grains_oz</code></li>
         <li style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">D_TOTAL (cup eq) into dairy_cup</code></li>
         <li style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">ADD_SUGARS (tsp eq) into added_sugars_tsp</code></li>
         <li style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">FWHOLEFRT into whole_fruits_cup</code></li>
         <li style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">VTOTALLEG into total_vegetables_cup</code></li>
         <li style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">VDRKGRLEG into greens_and_beans_cup</code></li>
         <li style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">PFALLPROTLEG into total_protein_foods_oz</code></li>
         <li style="margin-bottom:5px;"><code style="padding:5px;background:#F0E0F0">PFSEAPLANTLEG into dairy_cup</code></li>
        </ul>
        <h4>2) Densities calculation</h4>
        <p>The appropriate ratios are constructed for each individual. Usually these are the ratios of the <strong>dietary constituents to 1000 kcal of energy, with the exception of fatty acids </strong>.
            <ul> <li>Fatty acids use the ratio of the sum of monounsaturated and polyunsaturated fatty acids to saturated fatty acids.</li> 
                <li>Also, two components (saturated fat and added sugars) are expressed on a percent of calories basis.</li>
                <li>To convert to a percent of calories basis, grams of saturated fat should be multiplied by 9 to convert g to kcal, and added sugars should be multiplied by 16 to convert teaspoons to kcal, prior to dividing by total energy.</li>
            </ul
</p>
   <ul>
    <li> Density of each component except (Fatty acids,  added sugar and sturated fat:<br><br>
$\large{density\_x = \frac{dietary\_constituent}{dietary\_constituent}\times{1000}}$

</li>
    <li>
        Fatty acid densities:<br><br>
$\large {fatty\_acid\_density\_x = \frac{monounsaturated\_fats\_g + polyunsaturated\_fats\_g}{saturated\_fats\_g}}$
    
</li>
<li>
        Saturated fatty acids density (<strong>grams of saturated fat should be multiplied by 9 to convert g to kcal</strong>)<br><br>
$\large{ density\_saturated\_fatty\_acids\_x = \frac{saturated\_fats\_g \times 9}{energy\_kcal}}$
        
</li>
    <li>
        Added sugars density (<strong>added sugars should be multiplied by 16 to convert tsp to kcal </strong>):<br><br>
$\large{ density\_added\_sugars\_x = \frac{added\_sugars\_tsp \times 16}{energy\_kcal}}$
    
</li>
</ul>
<h4>3) Scoring according to HEI Scoring Algorithm:</h4>
<table class="table table-sm bg-white table-bordered">
  <colgroup><col>
  <col>
  <col>
  </colgroup><colgroup style="border-left: 3px solid #ccc;"><col><col></colgroup>
  <colgroup style="border-start: 3px solid #ccc;"><col><col></colgroup>
  <colgroup><col>
  <col>
</colgroup><thead class="table-dark">
  <tr>
    <th scope="col">Component</th>
    <th scope="col">Dietary Constituents</th>
    <th scope="col">Maximum points</th>
    <th scope="colgroup">Standard for maximum score</th>
    <th scope="col">Standard for minimum score of zero</th>
  
  </tr>
</thead>

  <tr>
	  <th colspan="7" scope="rowgroup" align="left">From FPED (or other food-based database)</th>
  </tr>
  <tr>
    <td>Total Fruits</td>
    <td>Total Fruits</td>
    <td>5</td>
    <td>≥0.8 cup equiv. per 1,000 kcal</td>
    <td>No Fruits </td>
    
  </tr>
  <tr>
    <td>Whole Fruits</td>
    <td>Citrus, Melons, Berries + Other Intact Fruits</td>
    <td>5</td>
    <td>≥0.4 cup equiv. per 1,000 kcal</td>
    <td>No Whole Fruits</td>
   
  </tr>
  <tr>
    <td>Total Vegetables</td>
    <td>Total Vegetables + Legumes (Beans and Peas) in cup equivalents</td>
    <td>5</td>
    <td>≥1.1 cup equiv. per 1,000 kcal</td>
    <td>No Vegetables </td>
   
  </tr>
  <tr>
    <td>Greens and Beans</td>
    <td>Dark Green Vegetables + Legumes (Beans and Peas) in cup equivalents</td>
    <td>5</td>
    <td>≥0.2 cup equiv. per 1,000 kcal</td>
    <td>No Dark Green Vegetables or Legumes</td>
   
  </tr>
  <tr>
    <td>Whole Grains</td>
    <td>Whole Grains</td>
    <td>10</td>
    <td>≥1.5 oz equiv. per 1,000 kcal</td>
    <td>No Whole Grains</td>
    
  </tr>
  <tr>
    <td>Dairy</td>
    <td>Total Dairy</td>
    <td>10</td>
    <td>≥1.3 cup equiv. per 1,000 kcal</td>
    <td>No Dairy </td>
    
  </tr>
  <tr>
    <td>Total Protein Foods</td>
    <td>Total Meat, Poultry, and Seafood (including organ meats and cured meats) + Eggs + Nuts and Seeds + Soy + Legumes (Beans and Peas) in oz equivalents</td>
    <td>5 </td>
    <td>≥2.5 oz equiv. per 1,000 kcal</td>
    <td>No Protein Foods </td>

  </tr>
  <tr>
    <td>Seafood and Plant Proteins</td>
    <td>Seafood (high in omega-3) + Seafood (low in omega-3) + Soy + Nuts and Seeds + Legumes (Beans and Peas) in oz equivalents</td>
    <td>5</td>
    <td>≥0.8 oz equiv. per 1,000 kcal</td>
    <td>No Seafood or Plant Proteins</td>
 
  </tr>
  <tr>
    <td>Refined Grains</td>
    <td>Refined Grains</td>
    <td>10</td>
    <td>≤1.8 oz equiv. per 1,000 kcal</td>
    <td>≥4.3 oz equiv. per 1,000 kcal </td>

  </tr>
  <tr>
    <td>Added Sugars</td>
    <td>Added Sugars</td>
    <td>10</td>
    <td>≤6.5% of energy</td>
    <td>≥26% of energy</td>

  </tr>
</tbody>
<tbody>
  <tr>
    <th colspan="7" scope="rowgroup" align="left">From FNDDS (or other nutrient database)</th>
  </tr>
  <tr>
    <td>Sodium</td>
    <td>Sodium</td>
    <td>10 </td>
    <td>≤1.1 gram per 1,000 kcal</td>
    <td>≥2.0 grams per 1,000 kcal</td>

  </tr>
  <tr>
    <td>Saturated Fats</td>
    <td>Total Saturated Fatty Acids</td>
    <td>10</td>
    <td>≤8% of energy</td>
    <td>≥16% of energy</td>

  </tr>
  <tr>
    <td>Fatty Acids</td>
    <td>(Total Monounsaturated Fatty Acids + Total Polyunsaturated Fatty Acids)/Total Saturated Fatty Acids</td>
    <td>10</td>
    <td>(PUFAs + MUFAs)/SFAs ≥2.5</td>
    <td>(PUFAs + MUFAs)/SFAs ≤1.2</td>

  </tr>
</tbody>
</table>
<p>The HEI-2020 components and scoring standards are the same as the HEI-2015. Intakes between the minimum and maximum standards are scored proportionately. The total HEI score is the sum of the adequacy components (i.e. foods to eat more of for good health) and moderation components (i.e. foods to limit for good health).</p>
<ul>
    <li>
        Scoring of Adequacty components (higer quantity required for good health):
        Following the formula below, When a score exceeds the maximum or falls below the minimum, it is clipped or capped to the respective maximum or minimum scoring value (<strong>Max points or 0</strong>).
        If the score is above the standard for maximum scoring, it is set to the maximum points.
        If the score is below the standard for minimum scoring, it is set to the minimum which s 0. 
        Intakes between the minimum and maximum standards are scored proportionately.<br><br>
$\large{Adequacy\_component\_score = \frac{X - Standard\_for\_min\_score}{Standard\_for\_max\_score - Standard\_for\_min\_score} \times max\_score}$
<br>Where  X  is the current observation of adequacy component. max_score is either 5 or 10.<br><br>
</li>
        <li>
        Scoring of Moderation components (lower quantity required for good health):
        Following the formula below, When a score falls below the standard for maximum scoring or exceeds the standard for minimum scoring of zero, it is clipped or capped to the respective <strong>maximum points or 0 </strong>.
        If the score is below  the standard maximum, it is set to the maximum points.
        If the score is above the standard for minimum scoring, it is set to the minimum which is 0.
        Intakes between the minimum and maximum standards are scored proportionately.<br><br>
$\large{Moderation\_component\_score = \frac{Standard\_for\_min\_score - X}{Standard\_for\_min\_score - Standard\_for\_max\_score} \times max\_score}$
<br>
where  x is the current observation of moderation component. max_score is either 5 or 10.<br><br>
    </li>
    <li>
        The component scores are summed to calculate the total score to construct the final Healthy Eating Index (HEI).
    </li>
    <li> The first dietary recall interview is conducted in-person at the Mobile Examination Center (MEC), and the second interview is collected via telephone 3 to 10 days later. To calculate the HEI index, the mean of the HEI values from both interviews is taken. Additionally, some sequence numbers (SEQN) are present in the Dietary Interview - Individual Foods, First Day (P_DR1IFF) but not in the Dietary Interview - Individual Foods, Second Day (P_DR2IFF), and vice versa. Specifically, 1,804 sequence numbers are present in P_DR1IFF but not in P_DR2IFF, and 2 sequence numbers are present in P_DR2IFF but not in P_DR1IFF. Merging files will create NaN values in the result file. To address this, missing HEI values are imputed using the existing values from the corresponding file(either P_DR1IFF or P_DR2IFF).  </li>
</ul>
<h3>References (and attribution) used in both this codebook:</h3>
<ul>
    <li><a href="https://epi.grants.cancer.gov/hei/hei-scoring-method.html"> HEI Scoring Algorithm</a></li>
    <li><a href="https://epi.grants.cancer.gov/hei/developing.html#2015">HEI-2020 & HEI–20151 Components & Scoring Standards</a></li>
    <li><a href="https://epi.grants.cancer.gov/hei/calculating-hei-scores.html">Steps for Calculating Healthy Eating Index Scores & Dietary  Constituents for HEI-2020</a> </li>
    <li><a href="https://github.com/AnnieKLamar/foodframe/tree/master">Github repo to calculate HEI, some corrections have been made to the code</a></li>
    <li><a href="https://www.ars.usda.gov/northeast-area/beltsville-md-bhnrc/beltsville-human-nutrition-research-center/food-surveys-research-group/docs/fped-databases/">FPED for Use with WWEIA, NHANES 2017-March 2020 Prepandemic</a></li>
    <li><a href="https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_DR1IFF.htm">Dietary Interview - Individual Foods, First Day (P_DR1IFF)</a></li>
<li><a href="https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_DR2IFF.htm">Dietary Interview - Individual Foods, Second Day (P_DR2IFF)</a></li>

</ul>


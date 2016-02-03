/*	This code create a new table newsalesemps from the sales table
located in Orion database and place the table in the temporary workspace WORK.
On execution, the newsalesemps is available for use.
*/

/*  =========== ARTICLE 1 =======*/

data work.newsalesemps;
	set orion.sales;
	where Salary >= 20000;
run;


/*Nicely print out data */
title 'New Sales Employees';
proc print data=work.newsalesemps;
run;

/* ==========  ARTICLE 2 ============ */
/*Classify the data based on job title and get summary statistics*/
proc means data=work.newsalesemps;
	class Job_Title;
	var Salary;
run;
title;

/* Create heirachical indexing using Job_title and Gender */
title 'Job Title by Gender distribution';
proc means data=work.newsalesemps;
	class Job_Title Gender;
	var Salary;
run;
title;



/* ===========  ARTICLE 3 ========= */
/* What is the gender distribution of  employee in each 
job position within the sales department? 
*/
proc sgplot data=WORK.NEWSALESEMPS;
	title 'Employee demographics analysis';

	/* Bar chart settings */
	hbar Job_Title /
	response=Salary 
	group=Gender 
	groupdisplay=Cluster stat=Mean 
	name='Bar';

	/* Response and category Axis settings */
	yaxis reverse grid;
	xaxis grid; 

	/* Legend Settings */
	keylegend / location=Inside across=1;
run;
ods graphics / reset;
title;


/* Which class of employee within the dept does 
the company spend more on in terms of salary? 
*/
proc sgplot data=WORK.NEWSALESEMPS;
	title 'Company spending as per Job_Title and Gender';
	vbar Job_Title / 
	response=Salary 
	group=Gender 
	groupdisplay=Cluster stat=Sum 
		name='Bar';

	yaxis grid;
	/* Legend Settings */
	keylegend / location=Inside across=1;
run;

ods graphics / reset;
title;

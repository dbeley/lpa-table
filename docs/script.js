$(document).ready(function() {
	//Only needed for the filename of export files.
	//Normally set in the title tag of your page.
	document.title='Linux Phone Apps Table - Explore data from LinuxPhoneApps.org';
  	var numbersType = $.fn.dataTable.absoluteOrderNumber( [
    	{ value: 'N/A', position: 'bottom' }
  	] );

	// DataTable initialisation
	$('#insights').DataTable(
		{
			"dom": 'BlfrtipQ',
			"buttons": [
				'copy',
        		'csv',
				'excel',
				'print',
				'colvis'
			],
			"paging": true,
			"autoWidth": true,
			"aLengthMenu": [[10, 25, 50, 100, 1000, -1], [10, 25, 50, 100, 1000, "All"]],
			"pageLength": 25,
            "scrollToTop": true,
			"order": [[2, 'desc']],
    		"columnDefs": [
      	  	  { type: numbersType, targets: [2, 3] },
              { targets: [3], render: DataTable.render.datetime('X', 'YYYY-MM-DD', 'en') },
      	      { width: "10%", targets: [0, 1] },
    		],
    		"responsive": true
		}
	);
});

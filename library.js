

function convertArrayCSV(arr){
	var result = '';
	for (int i = 0; i < arr.length; i++){
		result += arr.join(',') + '\n';
	}
	alert(result);
}
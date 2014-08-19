var fs = require('fs');
var obj = JSON.parse(fs.readFileSync('npm-datatables.json', 'utf8'));
var result = []
obj.aaData.forEach(function (elem) {
    if (elem[1] != null)
        result.push('https://github.com/' + elem[1])
});

var outputFilename = 'repos.json';

fs.writeFile(outputFilename, JSON.stringify(result, null, 4), function (err) {
    if (err) {
        console.log(err);
    } else {
        console.log("JSON saved to " + outputFilename);
    }
}); 
const fs = require('fs');
const crypto = require('crypto');
const hash = crypto.createHash('sha256');

const filename = process.argv[2] || 'data.csv';
console.log(`generate from ${filename}`);
const buffer = fs.readFileSync(filename);
const data = buffer.toString().split('\n');
let map = {};
for (let i in data) {
  if (data[i].length < 1) continue;
  const a = data[i].split(',');
  const student_id = a.shift();
  map[student_id] = a;
  // console.log(student_id, a);
}
// console.log(data);

// console.log(map);
try {
  fs.mkdirSync('build');
} catch (e) {
}

const map_str = JSON.stringify(map);
hash.update(map_str);
const data_var_name = `window._canvas_auto_rubric_data_${hash.digest('hex').
    substring(0, 6)}`;
fs.writeFileSync('build/index.js', [
  `${data_var_name} = ${map_str};`,
  `(`,
  fs.readFileSync('template.js'),
  `)(${data_var_name});`
].join('\n'));

console.log('successfully generated build/index.js');


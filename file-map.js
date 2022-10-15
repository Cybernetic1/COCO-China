const names = ["Claris", "Abeer", "Pete", "Eric"];

// Get all the files:
const files = document.querySelectorAll('div[class="File"]');
console.log("Total files = ", files.length);

for (const file of files) {
	file.contribs = [];
	for (var i = 0; i < 4; ++i) {
		file.contribs.push(100 * Math.random());
		}
	}

// Add event listeners to group of radio buttons:
const radioButtons = document.querySelectorAll('input[name="person"]');

for (const radioButton of radioButtons) {
	radioButton.addEventListener('change', showPerson);
	}

function showPerson(e) {
	// console.log(e);
	if (this.checked) {
		document.getElementById("PersonPic").src = names[this.value] + ".png";
		document.getElementById("PersonStats").innerHTML = "Name: " + names[this.value] + "<br>Tokens: 10,000";
		for (const file of files) {
			var canvas = file.children[0];
			var ctx = canvas.getContext("2d");
			ctx.beginPath();
			ctx.fillStyle = "magenta";
			ctx.clearRect(0, 0, 300, 200);
			ctx.rect(0, 0, 3 * file.contribs[this.value], 200);
			ctx.fill();
			}
		}
	}

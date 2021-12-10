

const play_ai = () => {

	$.get("/play", { i: 0, j: 0, turn: 'ai' }, (response) => {

		console.log("--------------- IA --------------------");
		console.table(response);
		response = JSON.parse(response);
		const board = response["eval_board"];
		const keys = Object.keys(board);

		keys.forEach((tuple, index) => {
			var symbol = board[tuple]['symbol'];
			var value = board[tuple]['value']
			// console.log({ tuple, index, symbol, value });

			var play = tuple.replace("(", "");
			play = play.replace(")", "");
			play = play.replace(" ", "");
			play = play.split(",");
			const id = `${play[0]}${play[1]}`;

			if (symbol == "O") {

				var type = "circles";
			}
			else {
				var type = "cross";

			}

			if (symbol != undefined && !$(`#${id} span`).hasClass(type)) {

				play = play.map(item => {
					return parseInt(item);
				});

				$(`#${id}`).addClass(type);
				$(`#${id} span`).html("");

			} else {

				$(`#${id} span`).html(value);

			}

		});

		if (response["won"] == true)
			alert("WON")


		console.log("--------------- NOVA RODADA --------------------");
	});


}


$(document).ready(function () {

	for (var i = 0; i < 7; i++) {

		for (var j = 0; j < 7; j++)

			$(".board").append(`<cell id="${i}${j}" value="${i},${j}"> <span /></cell>`);

	}

	$.get("/start_game", { attack: 'True' }, (response) => {

		// console.log(response);
		const board = response["eval_board"];
		const keys = Object.keys(board);

		keys.forEach((tuple, index) => {
			var symbol = board[tuple]['symbol'];
			var value = board[tuple]['value']
			// console.log({ tuple, index, symbol, value });

			var play = tuple.replace("(", "");
			play = play.replace(")", "");
			play = play.replace(" ", "");
			play = play.split(",");
			const id = `${play[0]}${play[1]}`

			if (symbol != undefined) {

				if (symbol == "O")
					var type = "circles";
				else
					var type = "cross";

				play = play.map(item => {
					return parseInt(item);
				});

				$(`#${id}`).addClass(type);
				if (value == null)
					$(`#${id}`).html("");

			} else {

				$(`#${id}`).html(`<span>${value}</span>`);

			}

		});

	});


	$("cell").on("click", function (e) {

		e.preventDefault()

		var tuple = $(this).attr("value").split(",");

		$.get("/play", { i: parseInt(tuple[0]), j: parseInt(tuple[1]), turn: 'player' }, (response) => {

			console.log("--------------- PLAYER --------------------");
			console.table(response);
			response = JSON.parse(response);
			const board = response["eval_board"];
			const keys = Object.keys(board);

			keys.forEach((tuple, index) => {
				var symbol = board[tuple]['symbol'];
				var value = board[tuple]['value']
				// console.log({ tuple, index, symbol, value });

				var play = tuple.replace("(", "");
				play = play.replace(")", "");
				play = play.replace(" ", "");
				play = play.split(",");
				const id = `${play[0]}${play[1]}`;

				if (symbol == "O") {

					var type = "circles";
				}
				else {
					var type = "cross";

				}

				if (symbol != undefined && !$(`#${id} span`).hasClass(type)) {

					play = play.map(item => {
						return parseInt(item);
					});

					$(`#${id}`).addClass(type);
					$(`#${id} span`).html("");

				} else {

					$(`#${id} span`).html(value);

				}

			});

			if (response["won"] == true)
				alert("WON")
			else
				play_ai()

		});

	});

});

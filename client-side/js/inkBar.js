var InkLvl = InkLvl || {};

InkLvl.inkBar = (function() {
	var defaultRoundedCornerRdx = 10;
	var defaultBorderWidth      = 1;

	function validType(type) {
		if (type == 'color' || type == 'black') {
			return true;
		}

		return false;
	}

	function validFillLevel(fill) {
		return fill >= 0 && fill <= 100;
	}

	function validDimensions(w, h) {
		return w > 0 && h > 0;
	}

	function genSvgBeginTag(w, h) {
		return '<svg width="' + w + '" height="' + h + '">';
	}
	
	function genBackgroundRect(w, h) {
		w -= defaultBorderWidth*2;
		h -= defaultBorderWidth*2;

		var s1 = '<rect x="' + defaultBorderWidth + '" y="' + defaultBorderWidth + '" ';
		var s2 = 'rx="' + defaultRoundedCornerRdx + '" ry="' + defaultRoundedCornerRdx + '" ';
		var s3 = 'width="' + w + '" height="' + h + '" ';
		var s4 = 'style="fill:white;stroke:grey;stroke-width:' + defaultBorderWidth + ';opacity:1" />';
		
		return s1 + s2 + s3 + s4;
	}

	function genInkBars(w, h, type, fill) {
		var yOffset = defaultRoundedCornerRdx * 2 + defaultBorderWidth;
		var workHeight = h - yOffset - defaultBorderWidth;

		var barHeight = Math.round(workHeight*(fill/100));
		var yStartPos = yOffset + (workHeight - barHeight);
		barHeight -= 0.5;
		var barColors = [];
		if (type == 'color') {
			barColors = ['66,156,198', '189,33,115', '247,247,24'];
		} else if (type == 'black') {
			barColors = ['0,0,0'];
		}

		var barWidth = Math.floor((w - defaultBorderWidth*2 - defaultRoundedCornerRdx*2)/barColors.length);
		var barX = defaultRoundedCornerRdx + defaultBorderWidth;
		var result = '';
		for (var i = 0; i < barColors.length; ++i) {
			var s1 = '<rect x="' + barX + '" y="' + yStartPos + '" ';
			var s2 = 'width="' + barWidth + '" height="' + barHeight + '" ';
			var s3 = 'style="fill:rgb(' + barColors[i] + ');opacity:1" />';

			result += s1 + s2 + s3;
			barX += barWidth;
		}

		return result;
	}

	function genGridLines(w, h) {
		var yOffset = defaultRoundedCornerRdx * 2 + defaultBorderWidth;
		var lineStep = Math.floor((h - yOffset - defaultBorderWidth)/4);

		var result = '';
		for (var i = 0; i < 4; i++) {
			var yVal = (yOffset + lineStep*i);
			var color = i == 0 ? 'blue' : 'grey';
			var s1 = '<line x1="' + defaultBorderWidth + '" y1="' + yVal + '" ';
			var s2 = 'x2="' + (w - defaultBorderWidth) + '" y2="' + yVal + '" ';
			var s3 = 'style="stroke:' + color + ';stroke-width:' + defaultBorderWidth + '" />';

			result += s1 + s2 + s3;
		}

		return result;
	}

	function getSvgEndTag() {
		return '</svg>';
	}

	return {
		setDefaultBoarderWidth: function(bw) {
			defaultBorderWidth = bw;
		},

		setDefaultCornerRdx: function(cornerRdx) {
			defaultRoundedCornerRdx = cornerRdx;	
		},

		render: function(width, height, type, fillLevel) {
			if (validType(type) == false) {
				return 'Wrong type passed (' + type + ')!';
			}
		
			if (validFillLevel(fillLevel) == false) {
				return 'Incorrect ink/toner fill level!';
			}

			return genSvgBeginTag(width, height) + 
			       genBackgroundRect(width, height) + 
			       genInkBars(width, height, type, fillLevel) +
			       genGridLines(width, height) + 
			       getSvgEndTag();
		}
	};
})();

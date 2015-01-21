var InkLvl = InkLvl || {};

InkLvl.states = (function() {
	function hideAll() {
		$('#loading').addClass('hidden');
		$('#error').addClass('hidden');
		$('#ink-levels-display').addClass('hidden');
	}

	function loadOrReload() {
			hideAll();
			$('#loading').removeClass('hidden');
			$('#reload-info').attr('disabled','disabled');
	}

	var inkMapping = {
		'Black': {
			'css': '#black-ink-gadget',
			'js' : 'color'
		},

		'Tri-color': {
			'css': '#color-ink-gadget',
			'js' : 'black'
		}, 
	};

	function loadFinishedInt(data) {
		hideAll();
		$('#reload-info').removeAttr('disabled');

		if (data.error) {
			$('#error').html(data.error);
			$('#error').removeClass('hidden');
		} else {
			for (var i = 0; i < data.inkLevels.length; i++) {
				var m = inkMapping[data.inkLevels[i].color];
				if (m) {
					var l = data.inkLevels[i].level;
					$(m.css + ' .svg-placeholder').html(InkLvl.inkBar.render(112, 262, m.js, l));
					$(m.css + ' .ink-level-placeholder').html('<b>' + l + '%<b>');
				}
			}
				
			$('#printer-info').html('Drukarka: ' + data.printer);
			$('#updated-info').html('Ostatnia aktualizacja danych: ' + data.timestamp);
			$('#ink-levels-display').removeClass('hidden');
		}
	}

	return {
		reload: function() {
			loadOrReload();

			$.getJSON(InkLvl.config.reloadUri,loadFinishedInt);
		},
		initial: function() {
			loadOrReload();

			$.getJSON(InkLvl.config.infoUri, loadFinishedInt);

			$('#reload-info').click(this.reload);
		}
	};
})();

InkLvl.main = (function() {
	return function() {
		InkLvl.states.initial();
	};
})();

window.onload = InkLvl.main;

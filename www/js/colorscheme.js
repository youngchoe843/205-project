var colorscheme = (function()
{
  var colorwheel = [
    ['#ffebee','#fce4ec','#f3e5f5','#ede7f6','#e8eaf6','#e3f2fd','#e1f5fe','#e0f7fa','#e0f2f1','#e8f5e9','#f1f8e9','#f9fbe7','#fffde7','#fff8e1','#fff3e0','#fbe9e7','#efebe9','#fafafa','#eceff1'],
    ['#ffcdd2','#f8bbd0','#e1bee7','#d1c4e9','#c5cae9','#bbdefb','#b3e5fc','#b2ebf2','#b2dfdb','#c8e6c9','#dcedc8','#f0f4c3','#fff9c4','#ffecb3','#ffe0b2','#ffccbc','#d7ccc8','#f5f5f5','#cfd8dc'],
    ['#ef9a9a','#f48fb1','#ce93d8','#b39ddb','#9fa8da','#90caf9','#81d4fa','#80deea','#80cbc4','#a5d6a7','#c5e1a5','#e6ee9c','#fff59d','#ffe082','#ffcc80','#ffab91','#bcaaa4','#eeeeee','#b0bec5'],
    ['#e57373','#f06292','#ba68c8','#9575cd','#7986cb','#64b5f6','#4fc3f7','#4dd0e1','#4db6ac','#81c784','#aed581','#dce775','#fff176','#ffd54f','#ffb74d','#ff8a65','#a1887f','#e0e0e0','#90a4ae'],
    ['#ef5350','#ec407a','#ab47bc','#7e57c2','#5c6bc0','#42a5f5','#29b6f6','#26c6da','#26a69a','#66bb6a','#9ccc65','#d4e157','#ffee58','#ffca28','#ffa726','#ff7043','#8d6e63','#bdbdbd','#78909c'],
    ['#f44336','#e91e63','#9c27b0','#673ab7','#3f51b5','#2196f3','#03a9f4','#00bcd4','#009688','#4caf50','#8bc34a','#cddc39','#ffeb3b','#ffc107','#ff9800','#ff5722','#795548','#9e9e9e','#607d8b'],
    ['#e53935','#d81b60','#8e24aa','#5e35b1','#3949ab','#1e88e5','#039be5','#00acc1','#00897b','#43a047','#7cb342','#c0ca33','#fdd835','#ffb300','#fb8c00','#f4511e','#6d4c41','#757575','#546e7a'],
    ['#d32f2f','#c2185b','#7b1fa2','#512da8','#303f9f','#1976d2','#0288d1','#0097a7','#00796b','#388e3c','#689f38','#afb42b','#fbc02d','#ffa000','#f57c00','#e64a19','#5d4037','#616161','#455a64'],
    ['#c62828','#ad1457','#6a1b9a','#4527a0','#283593','#1565c0','#0277bd','#00838f','#00695c','#2e7d32','#558b2f','#9e9d24','#f9a825','#ff8f00','#ef6c00','#d84315','#4e342e','#424242','#37474f'],
    ['#b71c1c','#880e4f','#4a148c','#311b92','#1a237e','#0d47a1','#01579b','#006064','#004d40','#1b5e20','#33691e','#827717','#f57f17','#ff6f00','#e65100','#bf360c','#3e2723','#212121','#263238'],
    ['#ff8a80','#ff80ab','#ea80fc','#b388ff','#8c9eff','#82b1ff','#80d8ff','#84ffff','#a7ffeb','#b9f6ca','#ccff90','#f4ff81','#ffff8d','#ffe57f','#ffd180','#ff9e80'],
    ['#ff5252','#ff4081','#e040fb','#7c4dff','#536dfe','#448aff','#40c4ff','#18ffff','#64ffda','#69f0ae','#b2ff59','#eeff41','#ffff00','#ffd740','#ffab40','#ff6e40'],
    ['#ff1744','#f50057','#d500f9','#651fff','#3d5afe','#2979ff','#00b0ff','#00e5ff','#1de9b6','#00e676','#76ff03','#c6ff00','#ffea00','#ffc400','#ff9100','#ff3d00'],
    ['#d50000','#c51162','#aa00ff','#6200ea','#304ffe','#2962ff','#0091ea','#00b8d4','#00bfa5','#00c853','#64dd17','#aeea00','#ffd600','#ffab00','#ff6d00','#dd2c00'],]
  var hue_order = [5,14,9,0,2,15,7,12,1,3,6,8,10,13,4,11,16,17,18]
  var shade_order = [5,1,9,3,7,2,8,10,6,11,12,13,0]
  function get(count)
  {
    var scheme = [], i = 0
    var shades = Math.min(8, count / 16 + 1)
    var hues = Math.min(16, Math.ceil(1.0 * count / shades))
    for (var shade = 0; shade < shades && i < count; ++shade) for (var hue = 0; hue < hues && i < count; ++hue) { scheme.push(colorwheel[shade_order[shade]][hue_order[hue]]); ++i; }
    return scheme;
  }
  api = { get: (function(){return get})() }
  return api;
})()
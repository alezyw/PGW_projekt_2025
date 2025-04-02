window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, context) {
            const {
                classes,
                skala_kolorow,
                style,
                colorProp
            } = context.hideout;
            const value = feature.properties[colorProp];
            for (let i = 0; i < classes.length; ++i) {
                if (value > classes[i]) {
                    style.fillColor = skala_kolorow[i];
                }
            }
            return style;
        },
        function1: function(feature, context) {
            return context.hideout.includes(feature.properties.name);
        }
    }
});
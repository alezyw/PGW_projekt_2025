window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, context) {
            return context.hideout.includes(feature.properties.name);
        }
    }
});
import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "IGT.TilesCalcUtils", // Можно поменять имя расширения на более общее
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        
        // Список нод, к которым мы хотим применять магию
        const myNodes = ["IGT_SimpleTilesCalc", "IGT_ImageTilesCalc"];

        if (myNodes.includes(nodeData.name)) {
            
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);

                if (message) {
                    const updateOutput = (slotIndex, value, label) => {
                        if (this.outputs && this.outputs[slotIndex]) {
                            this.outputs[slotIndex].name = `${value} ${label}`;
                        }
                    };

                    if (message.tile_w)  updateOutput(0, message.tile_w[0], "width");
                    if (message.tile_h)  updateOutput(1, message.tile_h[0], "height");
                    if (message.overlap) updateOutput(2, message.overlap[0], "overlap");
                    if (message.total)   updateOutput(3, message.total[0], "tiles");
                }
            };
        }
    },
});
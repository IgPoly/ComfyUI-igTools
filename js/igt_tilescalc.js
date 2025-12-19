import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "IGT.TilesCalcUtils",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // Добавляем новые ноды в список прослушивания
        const myNodes = [
            "IGT_SimpleTilesCalc", 
            "IGT_ImageTilesCalc", 
            "IGT_ImageResizer", 
            "IGT_AspectRatioResizer",
            "IGT_IntMinMax",   // <--
            "IGT_FloatMinMax"  // <--
        ];

        if (myNodes.includes(nodeData.name)) {
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);

                if (message) {
                    let changed = false;

                    const updateOutput = (slotIndex, value, labelSuffix) => {
                        if (this.outputs && this.outputs[slotIndex]) {
                            let newText = labelSuffix ? `${value} ${labelSuffix}` : `${value}`;
                            const currentLabel = this.outputs[slotIndex].label || this.outputs[slotIndex].name;

                            if (currentLabel !== newText) {
                                this.outputs[slotIndex].label = newText;
                                changed = true;
                            }
                        }
                    };

                    // --- Логика для старых нод ---
                    if (message.tile_w)  updateOutput(0, message.tile_w[0], "width");
                    if (message.tile_h)  updateOutput(1, message.tile_h[0], "height");
                    if (message.overlap) updateOutput(2, message.overlap[0], "overlap");
                    if (message.total)   updateOutput(3, message.total[0], "tiles");

                    if (message.res_w) updateOutput(0, message.res_w[0], "width");
                    if (message.res_h) updateOutput(1, message.res_h[0], "height");
                    if (message.info)  updateOutput(2, message.info[0], ""); 

                    // --- Логика для новых Math нод ---
                    // Выход 0: Min, Выход 1: Max
                    if (message.min_val) updateOutput(0, message.min_val[0], ""); 
                    if (message.max_val) updateOutput(1, message.max_val[0], "");

                    if (changed && app.canvas.selected_nodes[this.id]) {
                        app.graph.setDirtyCanvas(true, true);
                    }
                }
            };
        }
    },
});
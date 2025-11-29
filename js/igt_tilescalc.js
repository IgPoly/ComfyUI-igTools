import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "IGT.TilesCalcUtils",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // Список твоих нод, к которым нужно применять скрипт
        const myNodes = ["IGT_SimpleTilesCalc", "IGT_ImageTilesCalc"];

        if (myNodes.includes(nodeData.name)) {
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                // Вызываем оригинальный метод, чтобы ничего не сломать
                onExecuted?.apply(this, arguments);

                if (message) {
                    let changed = false;

                    const updateOutput = (slotIndex, value, label) => {
                        // Проверяем существование выхода
                        if (this.outputs && this.outputs[slotIndex]) {
                            const newText = `${value} ${label}`;
                            const currentLabel = this.outputs[slotIndex].label || this.outputs[slotIndex].name;

                            // Если текст отличается, обновляем
                            if (currentLabel !== newText) {
                                this.outputs[slotIndex].name = newText;
                                this.outputs[slotIndex].label = newText;
                                changed = true;
                            }
                        }
                    };

                    // Применяем данные, пришедшие из Python
                    if (message.tile_w)  updateOutput(0, message.tile_w[0], "width");
                    if (message.tile_h)  updateOutput(1, message.tile_h[0], "height");
                    if (message.overlap) updateOutput(2, message.overlap[0], "overlap");
                    if (message.total)   updateOutput(3, message.total[0], "tiles");

                    // Если были изменения, обновляем холст
                    if (changed) {
                        app.graph.setDirtyCanvas(true, true);
                    }
                }
            };
        }
    },
});
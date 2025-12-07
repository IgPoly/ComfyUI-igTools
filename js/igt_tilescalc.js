import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "IGT.TilesCalcUtils",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // Добавляем новую ноду в список
        const myNodes = ["IGT_SimpleTilesCalc", "IGT_ImageTilesCalc", "IGT_ImageResizer"];

        if (myNodes.includes(nodeData.name)) {
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);

                if (message) {
                    let changed = false;

                    const updateOutput = (slotIndex, value, labelSuffix) => {
                        if (this.outputs && this.outputs[slotIndex]) {
                            // Если labelSuffix не передан, используем само значение как лейбл
                            let newText = labelSuffix ? `${value} ${labelSuffix}` : `${value}`;
                            
                            const currentLabel = this.outputs[slotIndex].label || this.outputs[slotIndex].name;

                            if (currentLabel !== newText) {
                                this.outputs[slotIndex].label = newText;
                                // Имя не меняем, чтобы не ломать связи при сохранении, меняем только визуальный label
                                // this.outputs[slotIndex].name = newText; 
                                changed = true;
                            }
                        }
                    };

                    // Логика для старых нод (TilesCalc)
                    if (message.tile_w)  updateOutput(0, message.tile_w[0], "width");
                    if (message.tile_h)  updateOutput(1, message.tile_h[0], "height");
                    if (message.overlap) updateOutput(2, message.overlap[0], "overlap");
                    if (message.total)   updateOutput(3, message.total[0], "tiles");

                    // Логика для новой ноды (Resizer)
                    // Выход 0: Width, Выход 1: Height, Выход 2: Info String
                    if (message.res_w) updateOutput(0, message.res_w[0], "width");
                    if (message.res_h) updateOutput(1, message.res_h[0], "height");
                    // Для Info просто выводим текст без суффикса
                    if (message.info)  updateOutput(2, message.info[0], ""); 

                    if (changed) {
                        // Если нода выбрана, обновляем панель свойств, если нужно
                        if(app.canvas.selected_nodes[this.id]) {
                            app.graph.setDirtyCanvas(true, true);
                        }
                    }
                }
            };
        }
    },
});
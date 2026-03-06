import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "IGT.TilesCalcUtils",
    
    // Внедряемся ДО регистрации нод в системе
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        

        if (nodeData.name === "IGT_LoadSingleImage") {
            const uploadExt = app.extensions.find(e => e.name === "Comfy.UploadImage");
            if (uploadExt && uploadExt.beforeRegisterNodeDef) {
                // Создаем фейковую копию данных, маскируясь под "LoadImage"
                const fakeData = Object.assign({}, nodeData, {name: "LoadImage"});
                // Вызываем системный скрипт ComfyUI, передавая ему нашу фейковую ноду
                uploadExt.beforeRegisterNodeDef(nodeType, fakeData, app);
            }
        }
        // -------------------------------------------------------------


        const myNodes = [
            "IGT_SimpleTilesCalc", 
            "IGT_ImageTilesCalc", 
            "IGT_ImageResizer", 
            "IGT_AspectRatioResizer",
            "IGT_IntMinMax",
            "IGT_FloatMinMax"
        ];

        // Если текущая нода есть в списке выше
        if (myNodes.includes(nodeData.name)) {
            const onExecuted = nodeType.prototype.onExecuted;
            
            // Переопределяем метод, который вызывается после выполнения ноды на сервере
            nodeType.prototype.onExecuted = function (message) {
                // Обязательно вызываем оригинальный метод, чтобы ничего не сломать
                onExecuted?.apply(this, arguments);

                if (message) {
                    let changed = false;

                    // Вспомогательная функция для обновления текста на выходах (точках) ноды
                    const updateOutput = (slotIndex, value, labelSuffix) => {
                        if (this.outputs && this.outputs[slotIndex]) {
                            // Формируем новый текст: "значение + суффикс" или просто "значение"
                            let newText = labelSuffix ? `${value} ${labelSuffix}` : `${value}`;
                            const currentLabel = this.outputs[slotIndex].label || this.outputs[slotIndex].name;

                            // Если текст отличается, обновляем его
                            if (currentLabel !== newText) {
                                this.outputs[slotIndex].label = newText;
                                changed = true;
                            }
                        }
                    };

                    // --- Применяем данные, пришедшие из Python (поле 'ui' в return) ---
                    
                    // Логика для старых нод (TilesCalc)
                    if (message.tile_w)  updateOutput(0, message.tile_w[0], "width");
                    if (message.tile_h)  updateOutput(1, message.tile_h[0], "height");
                    if (message.overlap) updateOutput(2, message.overlap[0], "overlap");
                    if (message.total)   updateOutput(3, message.total[0], "tiles");

                    // Логика для нод ресайза (Resizer)
                    if (message.res_w) updateOutput(0, message.res_w[0], "width");
                    if (message.res_h) updateOutput(1, message.res_h[0], "height");
                    // Информационная строка без суффикса
                    if (message.info)  updateOutput(2, message.info[0], ""); 

                    // Логика для новых математических нод (MinMax)
                    if (message.min_val) updateOutput(0, message.min_val[0], ""); 
                    if (message.max_val) updateOutput(1, message.max_val[0], "");

                    // Если были изменения, командуем холсту перерисоваться
                    if (changed && app.canvas.selected_nodes[this.id]) {
                        app.graph.setDirtyCanvas(true, true);
                    }
                }
            };
        }
        // -------------------------------------------------------------
    },
});

document.head.appendChild(cheatStyles);
// Элементы DOM
const slimeImage = document.getElementById("slime-image");
const spinButton = document.getElementById("spin-button");
const nameSpan = document.getElementById("name");
const chanceSpan = document.getElementById("chance");
const inventory = document.getElementById("inventory");
const backpackImage = document.getElementById("backpack-image");
const crafter = document.getElementById("crafter");
const hammerImage = document.getElementById("hammer-image");
const inventoryToggle = document.getElementById("inventory-toggle");
const crafterToggle = document.getElementById("crafter-toggle");
const saveButton = document.getElementById("save-button");
const loadButton = document.getElementById("load-button");
const resetButton = document.getElementById("reset-button");
const spinningEffect = document.getElementById("spinning-effect");
const rarityBadge = document.getElementById("rarity-badge");
const collectionsContainer = document.getElementById("collections");

// Состояние игры
let inventoryOpen = false;
let crafterOpen = false;
let multiplier = 10000000;
let autoSaveEnabled = true;
let autoSaveInterval;
let animationEnabled = true;
let isSpinning = false;
let spinQueue = 0;

// Добавляем инициализацию переменных бонусов
let harvestMultiplier = 1;
let spinCooldown = 1000;
let rareChanceBoost = 0;
let epicChanceBoost = 0;
let divineChanceMultiplier = 1;

let collectionsVisible = true;
let indexVisible = true;

// Добавляем в функцию initGame
document.getElementById('toggle-collections').addEventListener('click', toggleCollections);
document.getElementById('toggle-index').addEventListener('click', toggleIndex);

let activeEffects = {
    harvestMultiplier: 1,   // Множитель количества выпадающих слаймов
    spinCooldown: 1000,     // Время восстановления спина в мс
    rareChanceBoost: 0,     // Бонус к шансу редких слаймов
    epicChanceBoost: 0,     // Бонус к шансу эпических слаймов
    divineChanceBoost: 1,   // Множитель шанса божественных слаймов
    timeReduction: 0        // Сокращение времени восстановления
};

// Инициализация игры
function initGame() {
    // Гарантируем наличие свойства created
    CRAFTS.forEach(craft => {
        if (typeof craft.created === 'undefined') {
            craft.created = false;
        }
    });
    
    // Загрузка сохранения
    loadGame();
    
    // Настройка обработчиков событий
    spinButton.addEventListener("click", spin);
    inventoryToggle.addEventListener("click", toggleInventory);
    crafterToggle.addEventListener("click", toggleCrafter);
    saveButton.addEventListener("click", manualSave);
    loadButton.addEventListener("click", loadGame);
    resetButton.addEventListener("click", resetProgress);
    document.getElementById('animation-toggle').addEventListener('change', function(e) {
        animationEnabled = e.target.checked;
        console.log(`Анимация ${animationEnabled ? 'включена' : 'отключена'}`);
    });

    // Проверяем состояние коллекций
    checkCollections();
    
    // Рендерим коллекции
    renderCollections();
    renderIndex();

    updateActiveEffects();
    loadUIState()
    
    // Запуск автосохранения
    if (autoSaveEnabled) {
        startAutoSave();
    }
}

// Функция сброса прогресса
function resetProgress() {
    if (confirm("Вы уверены, что хотите сбросить весь прогресс? Все ваши данные будут удалены.")) {
        // Сбрасываем данные в памяти
        SLIMES.forEach(slime => slime.amount = 0);
        CRAFTS.forEach(craft => craft.created = false);
        COLLECTIONS.forEach(collection => {
            collection.completed = false;
            collection.claimed = false;
        });
        
        // Сбрасываем бонусы
        multiplier = 10000000;
        harvestMultiplier = 1;
        spinCooldown = 1000;
        rareChanceBoost = 0;
        epicChanceBoost = 0;
        divineChanceMultiplier = 1;
        
        // Удаляем сохранение
        localStorage.removeItem('slimeCollectorSave');
        
        // Обновляем интерфейс
        if (inventoryOpen) renderInventory();
        if (crafterOpen) renderCrafter();
        renderCollections();
        
        // Сбрасываем текущий слайм
        const defaultSlime = SLIMES[0];
        slimeImage.src = defaultSlime.image;
        nameSpan.textContent = defaultSlime.name;
        chanceSpan.textContent = defaultSlime.chance;
        rarityBadge.textContent = getRarityName(defaultSlime.rarity);
        rarityBadge.className = `rarity-badge ${defaultSlime.rarity}`;
        
        console.log("Прогресс сброшен!");
        renderIndex()
        renderActiveEffects();
    }
}

// Расширенный метод спин для обработки всех типов слаймов
function spin() {
    if (isSpinning) {
        spinQueue++;
        return;
    }

    isSpinning = true;
    spinButton.disabled = true;
    
    if (animationEnabled) {
        // Показываем анимацию вращения
        spinningEffect.style.display = "block";
        spinningEffect.style.animation = "none";
        setTimeout(() => {
            spinningEffect.style.animation = "spin 1s infinite linear";
        }, 10);
        
        // Анимированный спин
        let spinCount = 0;
        const spinInterval = setInterval(() => {
            const randomSlime = SLIMES[Math.floor(Math.random() * SLIMES.length)];
            
            // Проверяем, известен ли слайм
            const isKnown = randomSlime.amount > 0;
            
            // Устанавливаем изображение
            slimeImage.src = isKnown ? randomSlime.image : UNKNOWN_SLIME_IMAGE;
            
            // Устанавливаем имя
            nameSpan.textContent = isKnown ? randomSlime.name : "???";
            
            // Устанавливаем редкость
            if (isKnown) {
                rarityBadge.textContent = getRarityName(randomSlime.rarity);
                rarityBadge.className = `rarity-badge ${randomSlime.rarity}`;
            } else {
                rarityBadge.textContent = "???";
                rarityBadge.className = "rarity-badge unknown";
            }
            
            // Устанавливаем шанс
            chanceSpan.textContent = isKnown ? randomSlime.chance : "???";
            
            spinCount++;
            if (spinCount > 10) {
                clearInterval(spinInterval);
                selectFinalSlime();
            }
        }, 150);
    } else {
        // Мгновенный спин без анимации
        setTimeout(() => {
            selectFinalSlime();
        }, 50);
    }
}

// Функция для выбора финального слайма
function selectFinalSlime() {
    const maxRange = 10000000000;
    const randomNum = Math.floor(Math.random() * maxRange) + 1;
    
    let selectedSlime = null;
    let candidates = [];
    
    for (const slime of SLIMES) {
        let chanceValue = parseInt(slime.chance.split('/')[1]);
        
        // Применяем бустеры к шансам
        if (slime.rarity === "rare") {
            chanceValue = Math.max(1, Math.floor(chanceValue * (1 - activeEffects.rareChanceBoost)));
        } else if (slime.rarity === "epic") {
            chanceValue = Math.max(1, Math.floor(chanceValue * (1 - activeEffects.epicChanceBoost)));
        } else if (slime.rarity === "divine") {
            chanceValue = Math.max(1, Math.floor(chanceValue / activeEffects.divineChanceBoost));
        }
        
        if (randomNum % chanceValue === 0) {
            candidates.push(slime);
        }
    }
    
    selectedSlime = candidates.length > 0 ? 
        candidates[Math.floor(Math.random() * candidates.length)] : 
        SLIMES[0];
    
    // Применяем множитель количества
    const count = activeEffects.harvestMultiplier;
    selectedSlime.amount += count;
    
    if (animationEnabled) {
        setTimeout(() => {
            updateSlimeDisplay(selectedSlime);
            finishSpin();
        }, 500);
    } else {
        updateSlimeDisplay(selectedSlime);
        finishSpin();
    }
    
    console.log(`Получено ${count} ${selectedSlime.name}`);
}
function updateSlimeDisplay(slime) {
    slimeImage.src = slime.image;
    nameSpan.textContent = slime.name;
    chanceSpan.textContent = slime.chance;
    rarityBadge.textContent = getRarityName(slime.rarity);
    rarityBadge.className = `rarity-badge ${slime.rarity}`;
    
    if (slime.rarity !== "common") {
        console.log(`Вы получили редкого слайма: ${slime.name}!`);
    }
}
function finishSpin() {
    if (animationEnabled) {
        spinningEffect.style.display = "none";
    }
    
    isSpinning = false;
    
    if (spinQueue > 0) {
        spinQueue--;
        spin();
    } else {
        spinButton.disabled = false;
    }
    
    checkCollections();
    
    renderIndex();
    // Обновляем интерфейс коллекций
    renderCollections();

    if (inventoryOpen) renderInventory();
}
// Получение названия редкости
function getRarityName(rarity) {
    const names = {
        'common': 'Обычный',
        'uncommon': 'Необычный',
        'rare': 'Редкий',
        'epic': 'Эпический',
        'legendary': 'Легендарный',
        'mythic': 'Мифический',
        'divine': 'Божественный'
    };
    return names[rarity] || rarity;
}

// Переключение видимости инвентаря
function toggleInventory() {
    if (crafterOpen) {
        crafterOpen = false;
        crafter.style.display = "none";
        hammerImage.src = "assets/png/hammer.png";
    }
    
    inventoryOpen = !inventoryOpen;
    inventory.style.display = inventoryOpen ? "block" : "none";
    
    if (inventoryOpen) {
        renderInventory();
    }
}

// Отображение инвентаря
function renderInventory() {
    inventory.innerHTML = "";
    
    SLIMES.forEach(slime => {
        if (slime.amount > 0) {
            const slimeElement = document.createElement("div");
            slimeElement.className = "slime-item";
            slimeElement.innerHTML = `
                <img src="${slime.image}" alt="${slime.name}">
                <div>
                    <h3>${slime.name}</h3>
                    <p>Шанс: ${slime.chance}</p>
                    <p>Количество: ${slime.amount}</p>
                    <div class="rarity-badge ${slime.rarity}">${getRarityName(slime.rarity)}</div>
                </div>
            `;
            inventory.appendChild(slimeElement);
        }
    });
    
    if (inventory.innerHTML === "") {
        inventory.innerHTML = "<p>Ваш инвентарь пуст. Покрутите рулетку, чтобы получить слаймов!</p>";
    }
}

// Переключение видимости крафта
function toggleCrafter() {
    if (inventoryOpen) {
        inventoryOpen = false;
        inventory.style.display = "none";
        backpackImage.src = "assets/png/backpack.png";
    }
    
    crafterOpen = !crafterOpen;
    crafter.style.display = crafterOpen ? "block" : "none";
    
    if (crafterOpen) {
        renderCrafter();
    }
}

// Отображение рецептов крафта
function renderCrafter() {
    crafter.innerHTML = "";
    crafter.innerHTML = "";
    
    CRAFTS.forEach((craft, index) => {
        // Проверяем наличие свойства created
        if (typeof craft.created === 'undefined') {
        craft.created = false;
        }
        // ... остальной код ...

    
        const craftElement = document.createElement("div");
        craftElement.className = "craft-recipe";
        craftElement.innerHTML = `
            <h3>${craft.name}</h3>
            <p>${craft.effect}</p>
            ${craft.created 
            ? '<div class="crafted-badge">Уже создан!</div>' 
            : `<div class="craft-item">
                <img src="${craft.image}" alt="${craft.name}">
                <button class="craft-button" data-index="${index}">Создать</button>
                </div>`
            }
            <h4>Требуется:</h4>
        `;
        
        craft.cost.forEach(item => {
            const slime = SLIMES.find(s => s.name === item.name);
            const hasEnough = slime && slime.amount >= item.amount;
            
            const costElement = document.createElement("div");
            costElement.className = "craft-item";
            costElement.innerHTML = `
                <img src="${slime.image}" alt="${item.name}">
                <span>${item.name} - ${item.amount} (${slime ? slime.amount : 0}/${item.amount})</span>
                ${hasEnough ? "✅" : "❌"}
            `;
            craftElement.appendChild(costElement);
        });
        
        crafter.appendChild(craftElement);
    });
    
    // Добавляем обработчики для кнопок крафта
    document.querySelectorAll(".craft-button").forEach(button => {
        button.addEventListener("click", function() {
            const index = parseInt(this.getAttribute("data-index"));
            craftItem(index);
        });
    });
}

function renderActiveEffects() {
const effectsList = document.getElementById("effects-list");
effectsList.innerHTML = "";

const effects = [];

// Собираем эффекты от амулетов
CRAFTS.filter(craft => craft.created).forEach(craft => {
    effects.push({
        name: craft.name,
        description: craft.effect,
        icon: craft.image
    });
});

// Собираем эффекты от коллекций
COLLECTIONS.filter(c => c.claimed).forEach(collection => {
    effects.push({
        name: collection.name,
        description: `Коллекция: ${collection.reward}`,
        icon: collection.thumbnail
    });
});

// Добавляем системные эффекты
if (activeEffects.harvestMultiplier > 1) {
    effects.push({
        name: "Множитель урожая",
        description: `x${activeEffects.harvestMultiplier} слаймов за спин`,
        icon: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCI+PHBhdGggZD0iTTE5IDE5SDVWNWg3VjNINWMtMS4xIDAtMiAuOS0yIDJ2MTRjMCAxLjEuOSAyIDIgMmgxNGMxLjEgMCAyLS45IDItMnYtN2gtMnY3ek0xNCAzdjJoMy41OWwtOS44MyA5LjgzIDEuNDEgMS40MUwxOSA2LjQxVjEwaDJWM2gtN3oiLz48L3N2Zz4="
    });
}

if (activeEffects.timeReduction > 0) {
    effects.push({
        name: "Ускорение",
        description: `Восстановление на ${Math.round(activeEffects.timeReduction * 100)}% быстрее`,
        icon: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCI+PHBhdGggZD0iTTEzIDNoLTJ2OGg4di0yaC02VjN6bS0yLjI0IDEyLjc1bC0xLjQxLTEuNDFMMi40MSAxOC42bDcuMTkgNy4xOSAxLjQxLTEuNDEtNS43OC01Ljc5eiIvPjwvc3ZnPg=="
    });
}

// Рендерим эффекты
effects.forEach(effect => {
    const effectElement = document.createElement("div");
    effectElement.className = "active-effect";
    effectElement.innerHTML = `
        <img src="${effect.icon}" width="30" height="30">
        <div>
            <strong>${effect.name}</strong>
            <div>${effect.description}</div>
        </div>
    `;
    effectsList.appendChild(effectElement);
});

if (effects.length === 0) {
    effectsList.innerHTML = "<p>Нет активных эффектов</p>";
}
}

function renderIndex() {
const indexContainer = document.getElementById("slime-index");
if (!indexContainer) return;

indexContainer.innerHTML = "";

// Счетчики для статистики
const totalSlimes = SLIMES.length;
const collectedSlimes = SLIMES.filter(s => s.amount > 0).length;
const progressPercent = Math.round((collectedSlimes / totalSlimes) * 100);

// Заголовок с прогрессом
const progressHeader = document.createElement("div");
progressHeader.className = "panel-header";
progressHeader.innerHTML = `
    <h3>Прогресс: ${collectedSlimes}/${totalSlimes} (${progressPercent}%)</h3>
`;
indexContainer.appendChild(progressHeader);

// Контейнер для сетки слаймов
const gridContainer = document.createElement("div");
gridContainer.className = "slime-index-grid";
indexContainer.appendChild(gridContainer);

// Сортируем слаймы по редкости
const rarityOrder = ['divine', 'mythic', 'legendary', 'epic', 'rare', 'uncommon', 'common'];
const sortedSlimes = [...SLIMES].sort((a, b) => {
    return rarityOrder.indexOf(a.rarity) - rarityOrder.indexOf(b.rarity);
});

// Добавляем каждый слайм в индекс
sortedSlimes.forEach(slime => {
    const isKnown = slime.amount > 0;
    const item = document.createElement("div");
    item.className = `slime-index-item ${isKnown ? 'known' : 'unknown'}`;
    
    item.innerHTML = `
        <div class="slime-index-icon">
            ${isKnown 
                ? `<img src="${slime.image}" alt="${slime.name}" width="70" height="70">` 
                : '?'}
        </div>
        <div class="slime-index-name">${isKnown ? slime.name : '???'}</div>
        ${isKnown 
            ? `<div class="slime-index-rarity ${slime.rarity}">${getRarityName(slime.rarity)}</div>`
            : ''}
    `;
    
    // Добавляем тултип с информацией для известных слаймов
    if (isKnown) {
        item.title = `${slime.name}\nШанс: ${slime.chance}\nРедкость: ${getRarityName(slime.rarity)}`;
    }
    
    gridContainer.appendChild(item);
});
}

function updateActiveEffects() {
// Сбрасываем эффекты перед пересчетом
activeEffects = {
    harvestMultiplier: 1,
    spinCooldown: 1000,
    rareChanceBoost: 0,
    epicChanceBoost: 0,
    divineChanceBoost: 1,
    timeReduction: 0
};

// Применяем эффекты от созданных амулетов
CRAFTS.filter(craft => craft.created).forEach(craft => {
    switch(craft.name) {
        case "Амулет Урожая":
            activeEffects.harvestMultiplier = 2;
            break;
        case "Амулет Вечности":
            activeEffects.timeReduction = 0.5;
            break;
        case "Амулет Изобилия":
            activeEffects.epicChanceBoost = 0.3;
            break;
        case "Амулет Слаймов":
            activeEffects.rareChanceBoost = 0.2;
            break;
    }
});

// Применяем эффекты от завершенных коллекций
COLLECTIONS.filter(c => c.claimed).forEach(collection => {
    switch(collection.id) {
        case "starting":
            activeEffects.epicChanceBoost += 0.05;
            break;
        case "elemental":
            activeEffects.harvestMultiplier += 1;
            break;
        case "rare_ones":
            activeEffects.timeReduction += 0.3;
            break;
        case "all_common":
            activeEffects.rareChanceBoost += 0.1;
            break;
        case "mythic_set":
            activeEffects.divineChanceBoost *= 2;
            break;
    }
});

// Применяем сокращение времени восстановления
activeEffects.spinCooldown *= (1 - activeEffects.timeReduction);

// Обновляем отображение эффектов
renderActiveEffects();
}
// Создание предмета
function craftItem(index) {
    const craft = CRAFTS[index];
    
    if (craft.created) {
        console.log("Этот амулет уже создан!");
        return;
    }

    // Проверяем, хватает ли ресурсов
    let canCraft = true;
    craft.cost.forEach(item => {
        const slime = SLIMES.find(s => s.name === item.name);
        if (!slime || slime.amount < item.amount) {
            canCraft = false;
        }
    });
    
    if (canCraft) {
        try {
            // Списываем ресурсы
            craft.cost.forEach(item => {
                const slime = SLIMES.find(s => s.name === item.name);
                if (slime) {
                    slime.amount -= item.amount;
                }
            });
            
            // Применяем эффект
            applyCraftEffect(craft);
            console.log(`Вы создали: ${craft.name}!`);
            
            // Обновляем интерфейс
            renderCrafter();
            if (inventoryOpen) renderInventory();
            renderActiveEffects();
        } catch (e) {
            console.error("Ошибка при создании предмета:", e);
        }
    } else {
        console.log("Недостаточно материалов для создания!");
        const craftButton = document.querySelector(`.craft-button[data-index="${index}"]`);
        if (craftButton) {
            craftButton.classList.add('craft-error');
            setTimeout(() => craftButton.classList.remove('craft-error'), 500);
        }
    }
}

// Применение эффекта от крафта
// Обновляем функции для применения эффектов
function applyCraftEffect(craft) {
    craft.created = true;
    updateActiveEffects(); // Обновляем эффекты после создания
}
// Ручное сохранение
function manualSave() {
    saveGame();
    console.log("Игра сохранена вручную!");
}
function checkCollections() {
    COLLECTIONS.forEach(collection => {
        let allCompleted = true;
        
        collection.slimes.forEach(req => {
            const slime = SLIMES.find(s => s.name === req.name);
            if (!slime || slime.amount < req.amount) {
                allCompleted = false;
            }
        });
        
        collection.completed = allCompleted;
    });
}

// Отображение коллекций
function renderCollections() {
    collectionsContainer.innerHTML = "";
    
    COLLECTIONS.forEach(collection => {
        const collectionEl = document.createElement("div");
        collectionEl.className = "collection-item";
        
        // Рассчитываем прогресс
        let totalSlimes = 0;
        let collectedSlimes = 0;
        
        collection.slimes.forEach(req => {
            totalSlimes += req.amount;
            const slime = SLIMES.find(s => s.name === req.name);
            if (slime) {
                collectedSlimes += Math.min(slime.amount, req.amount);
            }
        });
        
        const progressPercent = (collectedSlimes / totalSlimes) * 100;
        
        collectionEl.innerHTML = `
            <img class="collection-thumbnail" src="${collection.thumbnail}" alt="${collection.name}">
            <div class="collection-details">
                <h3>${collection.name}</h3>
                <p>${collection.description}</p>
                
                <div class="collection-slimes">
                    ${collection.slimes.map(req => {
                        const slime = SLIMES.find(s => s.name === req.name);
                        const hasEnough = slime && slime.amount >= req.amount;
                        return `
                            <div class="collection-slime ${hasEnough ? 'completed' : ''}">
                                <img src="${slime ? slime.image : ''}" alt="${req.name}">
                                <span>${req.name} (${slime ? slime.amount : 0}/${req.amount})</span>
                            </div>
                        `;
                    }).join('')}
                </div>
                
                <div class="collection-progress">
                    <div class="progress-bar" style="width: ${progressPercent}%"></div>
                </div>
                
                <div class="collection-reward">Награда: ${collection.reward}</div>
                
                ${collection.completed 
                    ? collection.claimed 
                        ? `<div class="collection-status completed">Награда получена!</div>`
                        : `<button class="claim-button" data-id="${collection.id}">Получить награду</button>`
                    : `<div class="collection-status locked">Коллекция не завершена</div>`
                }
            </div>
        `;
        
        collectionsContainer.appendChild(collectionEl);
    });
    
    // Добавляем обработчики для кнопок получения наград
    document.querySelectorAll(".claim-button").forEach(button => {
        button.addEventListener("click", function() {
            const collectionId = this.getAttribute("data-id");
            claimCollectionReward(collectionId);
        });
    });
}

// Получение награды за коллекцию
function claimCollectionReward(collectionId) {
    const collection = COLLECTIONS.find(c => c.id === collectionId);
    
    if (!collection || !collection.completed || collection.claimed) {
        return;
    }
    
    // Помечаем коллекцию как завершенную
    collection.claimed = true;
    
    // Применяем бонус
    applyCollectionBonus(collection);
    
    // Обновляем интерфейс
    renderCollections();
    
    // Сохраняем игру
    saveGame();
    
    console.log(`Награда за коллекцию "${collection.name}" получена!`);
}



// Сохранение состояния UI
function saveUIState() {
const uiState = {
    collectionsVisible,
    indexVisible
};
localStorage.setItem('slimeUIState', JSON.stringify(uiState));
}

// Загрузка состояния UI
function loadUIState() {
const savedUI = localStorage.getItem('slimeUIState');
if (savedUI) {
    try {
        const uiState = JSON.parse(savedUI);
        collectionsVisible = uiState.collectionsVisible;
        indexVisible = uiState.indexVisible;
        
        // Применяем сохраненное состояние
        document.querySelector('.collections-area').style.display = 
            collectionsVisible ? 'block' : 'none';
        document.querySelector('.index-area').style.display = 
            indexVisible ? 'block' : 'none';
        
        // Обновляем текст кнопок
        document.getElementById('toggle-collections').textContent = 
            collectionsVisible ? 'Скрыть коллекции' : 'Показать коллекции';
        document.getElementById('toggle-index').textContent = 
            indexVisible ? 'Скрыть индекс' : 'Показать индекс';
    } catch (e) {
        console.error('Ошибка загрузки состояния UI', e);
    }
}
}





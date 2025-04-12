/**
 * Model Switcher для Vanna-Flask
 * Добавляет возможность выбора разных LLM-моделей в сайдбар
 */

(function() {
    // Store for available models and current selection
    let availableModels = {};
    let currentProvider = '';
    let currentModel = '';

    // Function to fetch available models
    async function fetchAvailableModels() {
        try {
            const response = await fetch('/api/v0/get_available_models');
            const data = await response.json();
            
            if (data.type === 'available_models') {
                availableModels = data.models;
                currentProvider = data.current_provider;
                currentModel = data.current_model;
                renderModelSelector();
            } else {
                console.error('Error fetching models:', data.error);
            }
        } catch (error) {
            console.error('Failed to fetch models:', error);
        }
    }

    // Function to change model
    async function changeModel(provider, model, btnElement) {
        try {
            // Показываем индикатор загрузки на кнопке
            const originalBtnText = btnElement.innerHTML;
            btnElement.innerHTML = '<span class="animate-pulse">Applying...</span>';
            btnElement.disabled = true;
            
            const response = await fetch('/api/v0/change_model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ provider, model }),
            });
            
            const data = await response.json();
            
            if (data.type === 'success') {
                currentProvider = data.provider;
                currentModel = data.model;
                
                // Update the UI to reflect the change
                updateSelectedModel();
                
                // Показываем подтверждение на кнопке
                const confirmationContainer = document.getElementById('model-change-confirmation');
                if (!confirmationContainer) {
                    const newConfirmationContainer = document.createElement('div');
                    newConfirmationContainer.id = 'model-change-confirmation';
                    newConfirmationContainer.className = 'mt-2 text-center text-sm text-green-600 animate-pulse';
                    newConfirmationContainer.innerHTML = `<div class="flex items-center justify-center">
                        <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        Model applied successfully!
                    </div>`;
                    btnElement.parentNode.appendChild(newConfirmationContainer);
                } else {
                    confirmationContainer.style.display = 'block';
                }
                
                // Меняем стиль кнопки на успешный
                btnElement.classList.remove('bg-blue-500', 'hover:bg-blue-600');
                btnElement.classList.add('bg-green-500', 'hover:bg-green-600');
                btnElement.innerHTML = 'Applied!';
                
                // Показываем уведомление
                showNotification(`Model changed to ${availableModels[provider][model]}`, 'success');
                
                // Восстанавливаем стиль кнопки через 2 секунды
                setTimeout(() => {
                    btnElement.classList.remove('bg-green-500', 'hover:bg-green-600');
                    btnElement.classList.add('bg-blue-500', 'hover:bg-blue-600');
                    btnElement.innerHTML = originalBtnText;
                    btnElement.disabled = false;
                    
                    // Скрываем подтверждение через 3 секунды
                    setTimeout(() => {
                        const confirmationEl = document.getElementById('model-change-confirmation');
                        if (confirmationEl) {
                            confirmationEl.style.display = 'none';
                        }
                    }, 3000);
                }, 2000);
            } else {
                console.error('Error changing model:', data.error);
                showNotification(`Error: ${data.error}`, 'error');
                
                // Восстанавливаем кнопку
                btnElement.innerHTML = originalBtnText;
                btnElement.disabled = false;
            }
        } catch (error) {
            console.error('Failed to change model:', error);
            showNotification('Failed to change model. Check console for details.', 'error');
            
            // Восстанавливаем кнопку
            if (btnElement) {
                btnElement.innerHTML = 'Apply';
                btnElement.disabled = false;
            }
        }
    }

    // Function to show a notification
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-md shadow-md z-50 ${
            type === 'success' ? 'bg-green-500' : 
            type === 'error' ? 'bg-red-500' : 'bg-blue-500'
        } text-white`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // Function to update the selected model in the UI
    function updateSelectedModel() {
        const providerSelect = document.getElementById('llm-provider-select');
        const modelSelect = document.getElementById('llm-model-select');
        
        if (providerSelect) {
            providerSelect.value = currentProvider;
        }
        
        if (modelSelect) {
            // First clear existing options
            modelSelect.innerHTML = '';
            
            // Then add new options for the selected provider
            if (availableModels[currentProvider]) {
                Object.entries(availableModels[currentProvider]).forEach(([id, name]) => {
                    const option = document.createElement('option');
                    option.value = id;
                    option.textContent = name;
                    option.selected = id === currentModel;
                    modelSelect.appendChild(option);
                });
            }
        }
    }

    // Function to render the model selector in the sidebar
    function renderModelSelector() {
        // Find the sidebar element
        const sidebar = document.getElementById('application-sidebar');
        if (!sidebar) {
            console.error('Sidebar not found');
            return;
        }
        
        // Ищем кнопку Training Data в сайдбаре
        // Мы ищем кнопку по тексту, так как у неё может не быть уникального ID
        const trainingDataButton = Array.from(sidebar.querySelectorAll('button')).find(
            button => button.textContent.includes('Training Data')
        );
        
        if (!trainingDataButton) {
            console.error('Training Data button not found');
            // Если кнопка не найдена, используем старый способ вставки после первого ul
            const sidebarUl = sidebar.querySelector('ul');
            if (!sidebarUl) {
                console.error('Sidebar list not found');
                return;
            }
            insertModelSelector(sidebarUl.parentNode, sidebarUl.nextSibling);
            return;
        }
        
        // Найдем родительский элемент li кнопки Training Data
        let parentElement = trainingDataButton;
        while (parentElement && parentElement.tagName.toLowerCase() !== 'li') {
            parentElement = parentElement.parentElement;
        }
        
        if (!parentElement) {
            console.error('Parent li element of Training Data button not found');
            return;
        }
        
        // Вставляем селектор моделей перед элементом li с кнопкой Training Data
        insertModelSelector(parentElement.parentNode, parentElement);
    }
    
    // Helper function to insert the model selector
    function insertModelSelector(parentElement, beforeElement) {
        // Create model selector container
        const modelSelectorContainer = document.createElement('div');
        modelSelectorContainer.className = 'p-4 border-t border-gray-200 dark:border-gray-700';
        modelSelectorContainer.innerHTML = `
            <div class="space-y-3">
                <h3 class="text-xs font-semibold uppercase text-gray-500 dark:text-gray-300">LLM Model</h3>
                
                <div class="space-y-2">
                    <label for="llm-provider-select" class="text-xs text-gray-500 dark:text-gray-300">Provider</label>
                    <select id="llm-provider-select" class="py-2 px-3 pr-9 block w-full border-gray-200 rounded-md text-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400">
                        ${Object.keys(availableModels).map(provider => 
                            `<option value="${provider}" ${provider === currentProvider ? 'selected' : ''}>${provider.charAt(0).toUpperCase() + provider.slice(1)}</option>`
                        ).join('')}
                    </select>
                </div>
                
                <div class="space-y-2">
                    <label for="llm-model-select" class="text-xs text-gray-500 dark:text-gray-300">Model</label>
                    <select id="llm-model-select" class="py-2 px-3 pr-9 block w-full border-gray-200 rounded-md text-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400">
                        ${currentProvider && availableModels[currentProvider] 
                            ? Object.entries(availableModels[currentProvider]).map(([id, name]) => 
                                `<option value="${id}" ${id === currentModel ? 'selected' : ''}>${name}</option>`
                            ).join('') 
                            : ''}
                    </select>
                </div>
                
                <button id="change-model-btn" class="py-2 px-3 inline-flex justify-center items-center gap-2 rounded-md border border-transparent font-semibold bg-blue-500 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all text-sm dark:focus:ring-offset-gray-800">
                    Apply
                </button>
            </div>
        `;
        
        // Insert before the specified element
        parentElement.insertBefore(modelSelectorContainer, beforeElement);
        
        // Add event listeners
        const providerSelect = document.getElementById('llm-provider-select');
        const modelSelect = document.getElementById('llm-model-select');
        const changeBtn = document.getElementById('change-model-btn');
        
        providerSelect.addEventListener('change', function() {
            const selectedProvider = this.value;
            currentProvider = selectedProvider;
            
            // Update model select options
            modelSelect.innerHTML = '';
            
            if (availableModels[selectedProvider]) {
                Object.entries(availableModels[selectedProvider]).forEach(([id, name]) => {
                    const option = document.createElement('option');
                    option.value = id;
                    option.textContent = name;
                    modelSelect.appendChild(option);
                });
                
                // Select first model by default
                const firstModelId = Object.keys(availableModels[selectedProvider])[0];
                modelSelect.value = firstModelId;
            }
        });
        
        changeBtn.addEventListener('click', function() {
            const selectedProvider = providerSelect.value;
            const selectedModel = modelSelect.value;
            
            if (selectedProvider && selectedModel) {
                changeModel(selectedProvider, selectedModel, this);
            }
        });
    }

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        // Wait a bit to ensure the sidebar is fully loaded
        setTimeout(fetchAvailableModels, 500);
    });
})(); 
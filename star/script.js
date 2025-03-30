// Global variable to store all skill data after fetching
let allSkillsData = [];

// DOM Elements
const skillTableBody = document.getElementById('skillTableBody');
const emCheckboxes = document.querySelectorAll('input[name="em"]');
const campCheckboxes = document.querySelectorAll('input[name="camp"]');
const anyNoteCheckbox = document.getElementById('filterAnyNote');
const noteMoveCheckboxes = document.querySelectorAll('input[name="note_move_filter"]');
const noteEffectRadioButtons = document.querySelectorAll('input[name="note_effect_filter"]');
const useNoteEffectMaxCheckbox = document.getElementById('useNoteEffectMax');
// CT Speed Filters
const filterAnyCTSpeed = document.getElementById('filterAnyCTSpeed');
const ctspeedSpecialCheckboxes = document.querySelectorAll('input[name="ctspeed_special"]');
const ctspeedTargetCheckboxes = document.querySelectorAll('input[name="ctspeed_target_filter"]');
const ctspeedEffectRadioButtons = document.querySelectorAll('input[name="ctspeed_effect_filter"]');
const useCTSpeedEffectMaxCheckbox = document.getElementById('useCTSpeedEffectMax');
const ctspeedDurationRadioButtons = document.querySelectorAll('input[name="ctspeed_duration_filter"]');

// --- Helper Function to Check note_move Match (Handles "または" and "と") ---
function checkNoteMoveMatch(skillNoteMove, filterValue) {
    if (!skillNoteMove) {
        return false;
    }

    // Use a regex to split by either "または" or "と", trimming whitespace
    const parts = skillNoteMove.split(/または|と/).map(part => part.trim()).filter(part => part.length > 0);

    // Check if the filterValue matches any of the parts
    return parts.includes(filterValue);
}
function checkCTSpeedTargetMatch(ctspeedTarget, filterValue) {
    if (!ctspeedTarget) return false;
    const parts = ctspeedTarget.split(/または|と/).map(part => part.trim()).filter(part => part.length > 0);
    return parts.includes(filterValue);
}

// --- Function to display skills in the table ---
function displaySkills(skillsToDisplay) {
    skillTableBody.innerHTML = '';

    if (skillsToDisplay.length === 0) {
        skillTableBody.innerHTML = '<tr><td colspan="9">沒有符合條件的技能。</td></tr>';
        return;
    }

    skillsToDisplay.forEach(skill => {
        if (skill.No === 'No') return; // 跳過標頭行

        const row = skillTableBody.insertRow();
        row.insertCell().textContent = skill.star || ''; // 第一欄：星星
        
        // 插入圖片欄
        const imgCell = row.insertCell();
        imgCell.innerHTML = `<img src="img/${skill.No}.png" style="height:70px; width:auto;">`;
        
        // 第三欄：名前，轉成超連結，顯示文字不變，連結到 https://twinklestarknights.wikiru.jp/?<名前>
        const nameCell = row.insertCell();
        const name = skill.char || '';
        nameCell.innerHTML = `<a href="https://twinklestarknights.wikiru.jp/?${name}" target="_blank">${name}</a>`;
        
        row.insertCell().textContent = skill.em || '';   // 第四欄：属性
        row.insertCell().textContent = skill.camp || ''; // 第五欄：陣営
        row.insertCell().textContent = skill.EX || '';   // 第六欄：スキル
        row.insertCell().textContent = skill.EX_cost || ''; // 第七欄：消費EX
        row.insertCell().textContent = skill.range || '';   // 第八欄：攻撃範囲
        row.insertCell().textContent = skill.skill || '';   // 第九欄：効果全文(Lv1)
    });
}


// --- Function to filter skills based on selected checkboxes ---
function filterAndDisplaySkills() {
    // 1. Get basic filter values
    const selectedEm = Array.from(emCheckboxes)
                            .filter(checkbox => checkbox.checked)
                            .map(checkbox => checkbox.value);
    const selectedCamp = Array.from(campCheckboxes)
                             .filter(checkbox => checkbox.checked)
                             .map(checkbox => checkbox.value);

    // 2. Get Note filter states
    const anyNoteFilterChecked = anyNoteCheckbox.checked;
    const selectedNoteMoveFilters = Array.from(noteMoveCheckboxes)
                                        .filter(checkbox => checkbox.checked)
                                        .map(checkbox => checkbox.value);
    const selectedNoteEffectFilter = document.querySelector('input[name="note_effect_filter"]:checked').value;
    const useMaxEffect = useNoteEffectMaxCheckbox.checked;
	// Get CT Speed filter states
	const anyCTSpeedFilterChecked = filterAnyCTSpeed.checked;
	const selectedCTSpeedSpecial = Array.from(ctspeedSpecialCheckboxes)
		.filter(checkbox => checkbox.checked)
		.map(checkbox => checkbox.value);
	const selectedCTSpeedTargets = Array.from(ctspeedTargetCheckboxes)
		.filter(checkbox => checkbox.checked)
		.map(checkbox => checkbox.value);
	const selectedCTSpeedEffectFilter = document.querySelector('input[name="ctspeed_effect_filter"]:checked').value;
	const useMaxCTSpeedEffect = useCTSpeedEffectMaxCheckbox.checked;
	const selectedCTSpeedDurationFilter = document.querySelector('input[name="ctspeed_duration_filter"]:checked').value;
    // 3. Filter the data
    const filteredSkills = allSkillsData.filter(skill => {
        if (skill.No === 'No') return false; // Skip header row

        // --- Basic Filters ---
        const emMatch = selectedEm.length === 0 || (skill.em && selectedEm.includes(skill.em));
        const campMatch = selectedCamp.length === 0 || (skill.camp && selectedCamp.includes(skill.camp));
        if (!emMatch || !campMatch) return false;

        // --- Note Filters ---
        let noteMovePass = true;
        let noteEffectPass = true;

        // Check if skill has any note data
        const skillHasNoteData = (skill.note_effect !== undefined && skill.note_effect !== null) ||
                                 (skill.note_move !== undefined && skill.note_move !== null && skill.note_move !== '');

        // a) Apply "包含任何Note移動效果" filter
        if (anyNoteFilterChecked && !skillHasNoteData) {
            return false; // Fails immediately if this filter is on and skill has no note data
        }

        // b) Apply specific note_move filters (Target filter)
        if (selectedNoteMoveFilters.length > 0) {
            if (!skill.note_move || !selectedNoteMoveFilters.some(filterValue => checkNoteMoveMatch(skill.note_move, filterValue))) {
                noteMovePass = false; // Must have note_move and match at least one specific filter if any are selected
            }
        }
        if (!noteMovePass) return false; // Fails if note_move filters don't pass
// CT Speed Filters
const hasCTSpeedEffect = skill.CTspeed_target !== undefined && skill.CTspeed_target !== null && skill.CTspeed_target !== '';
if (anyCTSpeedFilterChecked && !hasCTSpeedEffect) {
    return false;
}

// Check special conditions (AND condition among selected specials)
const ctspeedEffectValue = skill.CTspeed_effect ? parseFloat(skill.CTspeed_effect) : NaN;
const isSelfTarget = skill.CTspeed_target === '自身';
const isEnemyTarget = skill.CTspeed_target && skill.CTspeed_target.includes('敵');
if (selectedCTSpeedSpecial.length > 0) {
    let specialPass = false;
    for (const special of selectedCTSpeedSpecial) {
        if (special === 'enemy_delay' && isEnemyTarget) {
            specialPass = true;
        } else if (special === 'self_shorten' && isSelfTarget && ctspeedEffectValue >= 0) {
            specialPass = true;
        } else if (special === 'self_delay' && isSelfTarget && ctspeedEffectValue < 0) {
            specialPass = true;
        }
    }
    if (!specialPass) return false;
}

// Check target filters (OR condition)
if (selectedCTSpeedTargets.length > 0) {
    const targetMatch = selectedCTSpeedTargets.some(target => checkCTSpeedTargetMatch(skill.CTspeed_target, target));
    if (!targetMatch) return false;
}

// Check effect value filter
if (selectedCTSpeedEffectFilter !== '') {
    let effectValueToUse = skill.CTspeed_effect;
    if (useMaxCTSpeedEffect && skill.CTspeed_effect_max !== undefined && skill.CTspeed_effect_max !== null) {
        effectValueToUse = skill.CTspeed_effect_max;
    }
    const effectValueNum = parseFloat(effectValueToUse);
    if (isNaN(effectValueNum)) {
        return false;
    }
    if (selectedCTSpeedEffectFilter === 'negative') {
        if (effectValueNum >= 0) return false;
    } else {
        const filterMin = parseFloat(selectedCTSpeedEffectFilter);
        if (effectValueNum < filterMin) return false;
    }
}

	// Check duration filter
	if (selectedCTSpeedDurationFilter !== '') {
		const durationValue = parseInt(skill.CTspeed_duration, 10);
		if (isNaN(durationValue)) {
			return false;
		}
		if (selectedCTSpeedDurationFilter === '1') {
			if (durationValue !== 1) return false;
		} else if (selectedCTSpeedDurationFilter === '2-4') {
			if (durationValue < 2 || durationValue > 4) return false;
		} else if (selectedCTSpeedDurationFilter === '5+') {
			if (durationValue < 5) return false;
		} else if (selectedCTSpeedDurationFilter === '10+') {
			if (durationValue < 10) return false;
		} else if (selectedCTSpeedDurationFilter === '20+') {
			if (durationValue < 20) return false;
		} else if (selectedCTSpeedDurationFilter === '30+') {
			if (durationValue < 30) return false;
		}
	}
// c) Apply note_effect filter (Amount/Type filter)
        if (selectedNoteEffectFilter !== "") { // Only filter if "不過濾" is not selected
            let effectValueToUse = skill.note_effect; // Start with the base effect

            // Determine the correct value based on the "Use Max" checkbox
            if (useMaxEffect && skill.note_effect_max !== undefined && skill.note_effect_max !== null) {
                effectValueToUse = skill.note_effect_max;
            }

            // Now, check if we have a valid value to filter against
            if (effectValueToUse === undefined || effectValueToUse === null) {
                // If no valid effect value exists (base or max), it cannot pass any specific filter.
                noteEffectPass = false;
            } else {
                // We have a value, now apply the specific filter type
                if (selectedNoteEffectFilter === "special") {
                    // Filter wants "special", check if the value is NOT a number
                    const numericValue = parseFloat(effectValueToUse);
                    if (!isNaN(numericValue) && isFinite(numericValue)) {
                         // The value IS a number, so it fails the "special" filter.
                        noteEffectPass = false;
                    }
                    // If it's not a number, noteEffectPass remains true (implicit pass).
                } else {
                    // Filter wants a number ("0" through "9+")
                    const filterRequiredMin = parseInt(selectedNoteEffectFilter, 10); // 0, 1, ..., 8, 9
                    const actualValueNum = parseFloat(effectValueToUse);

                    // Check if the actual value is a valid number AND meets the requirement
                    if (isNaN(actualValueNum) || !isFinite(actualValueNum)) {
                        // The actual value is not a number, so it fails the numerical filter.
                        noteEffectPass = false;
                    } else if (actualValueNum < filterRequiredMin) {
                         // The actual value is a number, but it's less than the required minimum.
                        noteEffectPass = false;
                    }
                     // If it's a number and >= filterRequiredMin, noteEffectPass remains true (implicit pass).
                }
            }
        }
        // If the noteEffect filter was active and failed, noteEffectPass is now false.
        if (!noteEffectPass) return false; // Exit if note effect filter failed

        // If all checks passed (including implicit passes where filters weren't active)
        return true;
    });

    // 4. Display the filtered results
    displaySkills(filteredSkills);
}


// --- Function to fetch data and initialize ---
async function initialize() {
    try {
        const response = await fetch('star_knight_data.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const jsonData = await response.json();

        // Clean up potential BOM and normalize the header key 'No'
        if (jsonData.length > 0) {
            const firstKey = Object.keys(jsonData[0])[0];
            if (firstKey.charCodeAt(0) === 0xFEFF) { // Check for BOM
                const cleanedFirstKey = firstKey.substring(1);
                jsonData.forEach(item => {
                    if (item.hasOwnProperty(firstKey)) {
                        item[cleanedFirstKey] = item[firstKey];
                         // Only delete if keys are truly different
                        if(cleanedFirstKey !== firstKey) delete item[firstKey];
                    }
                 });
                // Ensure header row uses the cleaned key if it exists
                 if(jsonData[0][cleanedFirstKey] === 'No') {
                    jsonData[0].No = 'No'; // Use 'No' consistently
                 } else if (jsonData[0][cleanedFirstKey] === '\uFEFFNo'){ // Handle case where value also has BOM
                    jsonData[0].No = 'No';
                 }
             } else if (jsonData[0].hasOwnProperty("﻿No")) { // Explicit check for the known BOM'd key
                 jsonData.forEach(item => {
                    item.No = item["﻿No"];
                    delete item["﻿No"];
                 });
             }
        }

        allSkillsData = jsonData;

        // Initial display
        filterAndDisplaySkills();

        // Add event listeners to ALL relevant controls
        emCheckboxes.forEach(checkbox => checkbox.addEventListener('change', filterAndDisplaySkills));
        campCheckboxes.forEach(checkbox => checkbox.addEventListener('change', filterAndDisplaySkills));
        anyNoteCheckbox.addEventListener('change', filterAndDisplaySkills);
        noteMoveCheckboxes.forEach(checkbox => checkbox.addEventListener('change', filterAndDisplaySkills));
        noteEffectRadioButtons.forEach(radio => radio.addEventListener('change', filterAndDisplaySkills));
        useNoteEffectMaxCheckbox.addEventListener('change', filterAndDisplaySkills);
filterAnyCTSpeed.addEventListener('change', filterAndDisplaySkills);
ctspeedSpecialCheckboxes.forEach(checkbox => checkbox.addEventListener('change', filterAndDisplaySkills));
ctspeedTargetCheckboxes.forEach(checkbox => checkbox.addEventListener('change', filterAndDisplaySkills));
ctspeedEffectRadioButtons.forEach(radio => radio.addEventListener('change', filterAndDisplaySkills));
useCTSpeedEffectMaxCheckbox.addEventListener('change', filterAndDisplaySkills);
ctspeedDurationRadioButtons.forEach(radio => radio.addEventListener('change', filterAndDisplaySkills));

    } catch (error) {
        console.error("無法載入或解析技能資料:", error);
        skillTableBody.innerHTML = `<tr><td colspan="8">錯誤：無法載入技能資料。請檢查 star_knight_data.json 檔案是否存在、格式正確且為 UTF-8 編碼。 ${error.message}</td></tr>`;
    }
}

// Start the process when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initialize);
document.addEventListener('DOMContentLoaded', function () {
    const skillsArray = [];

    function addSkill() {
        const inputElement = document.getElementById('skillInput');
        const skillValue = inputElement.value.trim();

        if (skillValue === '') {
            alert('Please enter a skill.');
            return;
        }

        // Add the skill to the array
        skillsArray.push(skillValue);

        // Create a skill chip
        const skillChip = document.createElement('div');
        skillChip.className = 'skillChip';
        skillChip.innerHTML = `${skillValue}<span class="removeButton" onclick="removeSkill(this)"> x</span>`;

        // Append the skill chip to the skills container
        const skillsContainer = document.getElementById('skillsContainer');
        skillsContainer.appendChild(skillChip);

        // Clear the input
        inputElement.value = '';
    }

    function removeSkill(buttonElement) {
        const skillChip = buttonElement.parentNode;
        const skillValue = skillChip.textContent.trim();

        // Remove the skill from the array
        const index = skillsArray.indexOf(skillValue.slice(0, skillValue.length - 2));
        if (index !== -1) {
            skillsArray.splice(index, 1);
        }

        // Remove the skill chip from the container
        const skillsContainer = document.getElementById('skillsContainer');
        skillsContainer.removeChild(skillChip);
    }
    
    function isSkillsArrayEmpty() {
        
        return skillsArray.length === 0;
    }

    // Trigger the submitArray function on a different event (e.g., a custom button click)
    function submitArray() {
        let input = document.getElementById('skill_input');
        input.value=skillsArray;
        
    }
    document.getElementById('addSkillButton').addEventListener('click', addSkill);
    document.getElementById('skillsForm').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission
        if (isSkillsArrayEmpty()) {
            alert("Please add at least one skill.");
        } else {
            submitArray(); // Call the function to set the hidden input value
            this.submit(); // Now, proceed with the form submission
        }
    });
});
import React from "react";

const DropdownModel = ({ model_list, selected_model, on_model_change }) => {
    return (
        <div className="dropdown_model_container">
            <select
                className="dropdown_model_select"
                value={selected_model}
                onChange={(e) => on_model_change(e.target.value)}
            >
                <option value="">Select a model</option>
                {model_list.map((model, index) => (
                    <option key={index} value={model}>
                        {model}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default DropdownModel;

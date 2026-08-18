import "./Input.css";

function Input({ type, placeholder, value, onChange, name, autoComplete }) {
    return (
        <input
            className="input"
            type={type}
            placeholder={placeholder}
            value={value}
            onChange={onChange}
            name={name}
            autoComplete={autoComplete}
        />
    );
}

export default Input;
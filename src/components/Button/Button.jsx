import "./Button.css";

function Button({text,type="button"}){

    return(

        <button
        className="btn"
        type="submit"
        >
            {text}
        </button>
    )
}

export default Button;


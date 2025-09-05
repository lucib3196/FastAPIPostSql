

import clsx from "clsx"
type ButtonVariant = "primary" | "secondary" | "danger" | "success";
const variantClasses: Record<ButtonVariant, string> = {
    primary: "bg-indigo-500 text-white hover:bg-indigo-800",
    secondary: "bg-red-400 text-black hover:bg-red-500",
    danger: "bg-red-500 text-white hover:bg-red-600",
    success: "bg-green-500 text-white hover:bg-green-600",
};
type MyButtonProps = {
    name: string;
    variant?: ButtonVariant;
    className?: string;
    onClick?: () => void;
    disabled?: boolean;
    btype?: "button" | "submit" | "reset";
};

export const MyButton = ({ name, variant = "primary", className, onClick, disabled, btype = "button" }: MyButtonProps) => {
    return (
        <button
            type={btype}
            onClick={onClick}
            disabled={disabled}
            className={clsx(
                "px-4 py-2 rounded font-semibold transition-colors duration-300 ease-in-out hover:-translate-y-1 hover:scale-110",
                variantClasses[variant],
                disabled && "opacity-50 cursor-not-allowed",
                className
            )}
        >
            {name}
        </button>
    )
}
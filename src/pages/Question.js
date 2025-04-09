import { useParams, useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";

const fields = ["vclass", "fueltype", "drive", "trany", "cylinders"];

const fieldLabels = {
    vclass: "What vehicle class do you prefer?",
    fueltype: "What type of fuel?",
    drive: "Preferred drive type?",
    trany: "Preferred transmission?",
    cylinders: "How many cylinders?"
};

function Question() {
    const { id } = useParams();
    const questionIndex = parseInt(id) - 1;
    const navigate = useNavigate();
    const location = useLocation();

    const [answers, setAnswers] = useState(location.state?.answers || {});
    const [selectedLabel, setSelectedLabel] = useState("");
    const [options, setOptions] = useState([]);
    const [loading, setLoading] = useState(true);

    const currentField = fields[questionIndex];
    const label = fieldLabels[currentField];
    const progress = ((questionIndex + 1) / fields.length) * 100;

    useEffect(() => {
        const fetchOptions = async () => {
            setLoading(true);
            try {
                const response = await fetch(`http://localhost:8080/options/filter/${currentField}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(answers)
                });

                const data = await response.json();
                setOptions(data.options || []);
            } catch (error) {
                console.error("Error fetching options:", error);
                setOptions([]);
            } finally {
                setLoading(false);
            }
        };

        fetchOptions();
    }, [questionIndex]);

    useEffect(() => {
        const existing = answers[currentField];
        if (Array.isArray(existing)) {
            const matched = options.find(opt => opt.values.includes(existing[0]));
            if (matched) {
                setSelectedLabel(matched.label);
            }
        } else if (typeof existing === "string") {
            setSelectedLabel(existing);
        }
    }, [options]);

    const handleNext = () => {
        const selected = options.find(opt => opt.label === selectedLabel);

        if (!selected || !selected.values || selected.values.length === 0) {
            alert("Please select an option.");
            return;
        }

        const updatedAnswers = {
            ...answers,
            [currentField]: selected.values
        };

        setAnswers(updatedAnswers);

        if (questionIndex + 1 < fields.length) {
            navigate(`/question/${questionIndex + 2}`, {
                state: { answers: updatedAnswers }
            });
        } else {
            fetch("http://localhost:8080/recommend", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(updatedAnswers)
            })
                .then((res) => res.json())
                .then((data) => {
                    navigate("/results", {
                        state: { recommendations: data.recommendations }
                    });
                })
                .catch((err) => {
                    console.error("Request error:", err);
                    alert("Something went wrong while fetching recommendations.");
                });
        }
    };

    const handleBack = () => {
        if (questionIndex === 0) {
            navigate("/");
        } else {
            navigate(`/question/${questionIndex}`, {
                state: { answers }
            });
        }
    };


    const handleReset = () => {
        const confirmReset = window.confirm("Are you sure you want to reset and start over?");
        if (confirmReset) {
            navigate("/question/1", {
                state: { answers: {} }
            });
        }
    };

    return (
        <div className="h-screen flex flex-col items-center justify-center bg-cover bg-center text-white"
             style={{ backgroundImage: "url('/background.png')" }}>
            <div className="absolute top-0 left-0 w-full bg-gray-700 h-3">
                <div className="bg-blue-500 h-3 transition-all" style={{ width: `${progress}%` }}></div>
            </div>

            <div className="bg-black bg-opacity-80 p-8 rounded-lg shadow-lg w-96 mt-10">
                <h2 className="text-2xl font-semibold mb-4">{label}</h2>

                {loading ? (
                    <p className="text-gray-300 mb-4">Loading options...</p>
                ) : (
                    <>
                        <select
                            value={selectedLabel}
                            onChange={(e) => setSelectedLabel(e.target.value)}
                            className="w-full p-2 border rounded mb-4 text-black"
                        >
                            <option value="" disabled>Select an option</option>
                            {options.map((opt, index) => (
                                <option key={index} value={opt.label}>{opt.label}</option>
                            ))}
                        </select>

                        <div className="flex justify-between gap-2 mb-4">
                            <button
                                onClick={handleBack}
                                disabled={questionIndex === 0}
                                className="w-full bg-gray-500 text-white py-2 rounded hover:bg-gray-700 transition disabled:opacity-50"
                            >
                                Back
                            </button>
                            <button
                                onClick={handleReset}
                                className="w-full bg-red-600 text-white py-2 rounded hover:bg-red-800 transition"
                            >
                                 Reset preferences
                            </button>
                        </div>

                        <button
                            onClick={handleNext}
                            className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-700 transition"
                        >
                            {questionIndex + 1 === fields.length ? "See Results" : "Next"}
                        </button>
                    </>
                )}
            </div>
        </div>
    );
}

export default Question;

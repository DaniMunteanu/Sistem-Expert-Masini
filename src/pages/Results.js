import { useLocation, useNavigate } from "react-router-dom";

function Results() {
    const { state } = useLocation();
    const navigate = useNavigate();
    const recommendedCars = state?.recommendations || [];

    const handleStartOver = () => {
        navigate("/");
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-start py-10 bg-cover bg-center text-white relative"
             style={{ backgroundImage: "url('/background.png')" }}>

            <h1 className="text-3xl font-bold mb-6 bg-black bg-opacity-80 p-4 rounded">Your Recommended Cars</h1>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {recommendedCars.map((car, index) => (
                    <div key={index} className="bg-black bg-opacity-80 p-6 shadow-lg rounded-lg text-center w-80">
                        <img
                            src={car.image}
                            alt={`${car.make} ${car.model}`}
                            className="w-full h-40 object-cover rounded mb-4"
                            onError={(e) => {
                                e.target.src = "/cars/default.jpg";
                            }}
                        />
                        <h2 className="text-xl font-semibold">{car.make} {car.model}</h2>
                        <p className="text-gray-300 text-sm">{car.year}</p>
                        <hr className="my-2 border-gray-600" />
                        <p className="text-gray-400 text-sm"><strong>Drive:</strong> {car.drive}</p>
                        <p className="text-gray-400 text-sm"><strong>Fuel:</strong> {car.fueltype}</p>
                        <p className="text-gray-400 text-sm"><strong>Class:</strong> {car.vclass}</p>
                        <p className="text-gray-400 text-sm"><strong>Transmission:</strong> {car.trany}</p>
                        <p className="text-gray-400 text-sm"><strong>Cylinders:</strong> {car.cylinders}</p>
                        <p className="text-blue-400 text-sm font-semibold mt-2">{car.match_level}</p>
                    </div>
                ))}
            </div>

            <button
                onClick={handleStartOver}
                className="absolute bottom-6 bg-black bg-opacity-70 hover:bg-opacity-90 text-white px-6 py-2 rounded-lg transition text-sm"
            >
                Back to Start
            </button>
        </div>
    );
}

export default Results;

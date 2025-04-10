import { Link } from "react-router-dom";

function Home() {
    return (
        <div className="h-screen flex flex-col items-center justify-center bg-cover bg-center text-white"
             style={{ backgroundImage: "url('/background.png')" }}>
            <div className="bg-black bg-opacity-80 p-10 rounded-lg shadow-lg text-center">
                <h1 className="text-5xl font-bold mb-4">Find Your Perfect Car</h1>
                <p className="text-lg text-gray-300 mb-6">Answer a few questions to get personalized recommendations.</p>
                <Link to="/question/1">
                    <button className="px-6 py-3 bg-blue-500 text-white rounded-lg text-lg shadow-lg hover:bg-blue-700 transition">
                        Start
                    </button>
                </Link>
            </div>
        </div>
    );
}

export default Home;

interface PopupProps {
  message: string;
  isVisible: boolean;
  onClose: () => void;
}

export default function Popup({ message, isVisible, onClose }: PopupProps) {
  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-xl">
        <div className="text-center">
          <p className="text-xl font-semibold text-gray-800 mb-4">{message}</p>
          <button
            onClick={onClose}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

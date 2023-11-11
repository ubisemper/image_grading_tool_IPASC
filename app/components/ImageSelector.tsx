import Image from "next/image";
import { useEffect } from "react";
import ImageViewer from "./ImageViewer";

type returnData = {
  data: string[];
  message: string;
};

interface ImageSelectorProps {
  fileNames: returnData;
  imageAlt: string;
  imageClasses: number[];
  selectedClass: number;
  onClassSelect: (classIndex: number) => void;
}

const handleIndex = (index: number) => {
  console.log(index);
};

export const ImageSelector = ({
  fileNames,
  imageAlt,
  imageClasses,
  selectedClass,
  onClassSelect,
}: ImageSelectorProps) => {
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      const key = Number(event.key);
      if (key >= 1 && key <= 5) {
        onClassSelect(key);
      }
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [onClassSelect]);

  return (
    <div className="flex flex-col items-center">
      <div className="relative">
        <ImageViewer onImageIndex={handleIndex} fileNames={fileNames.data} />
        {selectedClass !== 0 ? (
          <div
            className="absolute top-0 left-0 bg-gray-200 rounded-md p-2 text-lg"
            style={{ top: "-50px", left: "0" }}
          >
            Selected class: {`class ${selectedClass}`}
          </div>
        ) : (
          <div
            className="absolute top-0 left-0 bg-gray-200 rounded-md p-2 text-lg"
            style={{ top: "-50px", left: "0" }}
          >
            <p>No class selected</p>
          </div>
        )}
      </div>
      <div className="flex justify-center space-x-4 p-4 bg-gray-100">
        {imageClasses.map((grade, index) => (
          <button
            key={grade}
            className={`bg-gray-200 rounded-md p-4 text-lg ${
              selectedClass === index + 1 ? "bg-blue-400 text-black" : ""
            } hover:bg-blue-100`}
            onClick={() => onClassSelect(index + 1)}
          >
            {`class ${grade}`}
          </button>
        ))}
      </div>
    </div>
  );
};

"use client";

import Image from "next/image";
import { useEffect } from "react";
import ImageViewer from "./ImageViewer";
import { useRouter } from "next/navigation";

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
  onSubmit: () => void;
  onIndex: (index: number) => void;
}

export const ImageSelector = ({
  fileNames,
  imageAlt,
  imageClasses,
  selectedClass,
  onClassSelect,
  onSubmit,
  onIndex,
}: ImageSelectorProps) => {
  const handleIndex = (index: number) => {
    onIndex(index);
    console.log(index);
  };

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      const key = Number(event.key);
      if (key >= 1 && key <= 5) {
        onClassSelect(key);
      } else if (event.key === "Enter") {
        // Get a reference to the submit button
        const submitButton = document.getElementById("submit-button");
        if (submitButton) {
          // Programmatically click the submit button
          submitButton.click();
        }
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
              selectedClass === index + 1
                ? "bg-red-500 text-black"
                : "bg-gray-200"
            } hover:bg-blue-100`}
            onClick={() => onClassSelect(index + 1)}
          >
            {`class ${grade}`}
          </button>
        ))}
        <button
          id="submit-button"
          className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
          type="submit"
          onClick={onSubmit}
        >
          Submit
        </button>
      </div>
    </div>
  );
};

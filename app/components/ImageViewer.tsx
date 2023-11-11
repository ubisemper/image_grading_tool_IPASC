import { useState } from "react";
import ImageComponent from "@/app/components/ImageComponent";

type Props = {
  fileNames: string[];
  onImageIndex: (grade: number) => void;
};

const ImageViewer = ({ fileNames, onImageIndex }: Props) => {
  const [currentIndex, setCurrentIndex] = useState<number>(0);

  const nextImage = () => {
    let newIndex = currentIndex < fileNames.length - 1 ? currentIndex + 1 : 0;
    setCurrentIndex(newIndex);
    onImageIndex(newIndex);
  };

  const previousImage = () => {
    let newIndex = currentIndex > 0 ? currentIndex - 1 : fileNames.length - 1;
    setCurrentIndex(newIndex);
    onImageIndex(newIndex);
  };

  return (
    <div>
      {fileNames && fileNames.length > 0 ? (
        <div className="flex flex-col gap-y-2">
          <p>
            Image {currentIndex} of {fileNames.length - 1}
          </p>
          <ImageComponent filename={fileNames[currentIndex]} />
          <div className="flex flex-row justify-center">
            <button
              className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
              onClick={previousImage}
            >
              &lt; Previous
            </button>
            <button
              className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
              onClick={nextImage}
            >
              Next &gt;
            </button>
          </div>
        </div>
      ) : (
        <p>no images</p>
      )}
    </div>
  );
};

export default ImageViewer;

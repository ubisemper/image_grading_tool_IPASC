"use client";

import { useState, useEffect } from "react";
import Image from "next/image";
import DropDown from "@/app/components/DropDown";
import FolderSelector from "../components/FolderSelector";
import { ImageSelector } from "../components/ImageSelector";

type returnData = {
  data: string[];
  message: string;
};

const DashboardPage = () => {
  const [selectedFolder, setSelectedFolder] = useState("");
  const [selectedImageIndex, setSelectedImageIndex] = useState(0);
  const [selectedClass, setSelectedClass] = useState(0);

  const [fileNames, setFileNames] = useState<returnData | null>(null);
  const [folderNames, setFolderNames] = useState<returnData | null>(null);
  const [file, setFile] = useState<File | null>(null);

  const [taskId, setTaskId] = useState<string | null>();

  useEffect(() => {
    if (selectedFolder) {
      fetch(`/api/get_all_files_in_folder?folderName=${selectedFolder}`)
        .then((response) => response.json())
        .then((responseData) => setFileNames(responseData))
        .catch((error) => console.error("Error fetching data", error));
    }
    setSelectedImageIndex(0);
    console.log("IDX", selectedImageIndex);
  }, [selectedFolder]);

  useEffect(() => {
    fetch("/api/get_all_folder_names")
      .then((response) => response.json())
      .then((responseData) => setFolderNames(responseData))
      .catch((error) => console.error("Error fetching data", error));
  }, [file]);

  const handleSelect = (folderName: string) => {
    setSelectedFolder(folderName);
  };

  const handleFolderSelect = (folderName: string) => {
    setSelectedFolder(folderName);
    // TODO: Load images from selected folder
  };

  const handleImageSelect = (index: number) => {
    setSelectedImageIndex(index);
    setSelectedClass(0);
  };

  const handleGradeSelect = (index: number, grade: number) => {
    setSelectedClass(grade);
  };

  const handleSubmit = () => {
    // TODO: Submit image grades to server
  };

  const uploadToClient = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const i = event.target.files[0];
      setFile(i);
    }
  };
  const uploadToServer = async (event: React.MouseEvent<HTMLElement>) => {
    const body = new FormData();
    if (!file) {
      throw new Error("Image not made");
    }
    body.append("zipFile", file);
    const response = await fetch("/api/upload_zip", {
      method: "POST",
      body,
    });

    if (!response.ok) {
      console.error("failed to upload zip");
    }

    fetch("/api/get_all_folder_names")
      .then((response) => response.json())
      .then((responseData) => setFolderNames(responseData))
      .catch((error) => console.error("Error fetching data", error));
  };

  const handleGradeUpload = async () => {
    if (!fileNames || selectedClass === 0) {
      throw new Error("File names not provided | class not selected");
    }

    const response = await fetch(
      `/api/grade_image?fileName=${fileNames.data[selectedImageIndex]}&user=wytse&grade=${selectedClass}`
    );

    if (response.ok) {
      console.log("graded sucessfully");
    } else {
      console.log("FAILED");
    }
  };

  const handleZipTrigger = async (folderName: string) => {
    const response = await fetch(`/api/trigger_zip?folderName=${folderName}`, {
      method: "GET",
    });

    if (response.ok) {
      console.log("zip triggered successfully");
      const responseData = await response.json();
      setTaskId(responseData.data);
    } else {
      console.log("FAILED");
    }
  };

  const handleDownloadTrigger = async () => {
    const response = await fetch(`/api/download/${taskId}`, {
      method: "GET",
    });

    if (response.ok) {
      console.log("download triggered successfully");
      const downloadLink = await response;
      console.log("download link: ", downloadLink.url);
      window.open(downloadLink.url);
    } else {
      console.log("FAILED");
    }
  };

  console.log(fileNames?.data[selectedImageIndex]);

  return (
    <div className="flex flex-col md:flex-row h-screen">
      <div className="bg-gray-100 p-4 w-full md:w-1/5">
        <div className="flex items-center space-x-2 flex-col gap-y-2">
          <h3 className="font-semibold text-xl mb-10">
            PAI Data Labeling Tool
          </h3>

          <div className="flex flex-col w-full p-4 gap-y-3 bg-white rounded-lg shadow mb-4">
            <h5 className="font-bold mb-2">Upload zipfile</h5>
            <div className="flex flex-row items-center gap-x-2">
              <input type="file" name="testimage" onChange={uploadToClient} />
            </div>
            <button
              className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
              type="submit"
              onClick={uploadToServer}
            >
              Process
            </button>
          </div>

          <div className="flex flex-col w-full p-4 bg-white rounded-lg shadow gap-x-1 overflow-hidden">
            <span className="font-semibold">Selected:</span>
            <span className="truncate">{selectedFolder}</span>
          </div>
          <div className="flex w-full">
            <FolderSelector
              onSelect={handleFolderSelect}
              folderNames={folderNames}
            />
          </div>

          <button
            id="zip-trigger-button"
            className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
            type="submit"
            onClick={() => handleZipTrigger(selectedFolder)}
          >
            Trigger Zip
          </button>
          <button
            id="download-trigger-button"
            className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
            type="submit"
            onClick={handleDownloadTrigger}
          >
            Trigger Download
          </button>
        </div>
      </div>
      <div className="flex-1 flex items-center justify-center">
        {fileNames ? (
          <ImageSelector
            onIndex={(index) => handleImageSelect(index)}
            imageAlt="asd"
            imageClasses={[1, 2, 3, 4, 5]}
            fileNames={fileNames}
            onSubmit={handleGradeUpload}
            onClassSelect={(selectedClass: number) =>
              handleGradeSelect(selectedImageIndex, selectedClass)
            }
            selectedClass={selectedClass}
          />
        ) : (
          <p>Loading...</p>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;

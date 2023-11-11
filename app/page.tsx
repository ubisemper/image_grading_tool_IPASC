"use client";
import { useEffect, useState } from "react";
import ImageViewer from "@/app/components/ImageViewer";
import DropDown from "@/app/components/DropDown";

type returnData = {
  data: string[];
  message: string;
};
export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [fileNames, setFileNames] = useState<returnData | null>(null);
  const [folderNames, setFolderNames] = useState<returnData | null>(null);
  const [selectedFolder, setSelectedFolder] = useState<string | null>(null);
  const [selectedFileNames, setSelectedFileNames] = useState<string[] | null>(
    null
  );

  const [username, setUsername] = useState("");
  const [savedUserName, setSavedUserName] = useState("");

  const [grade, setGrade] = useState<number | null>(null);
  const [index, setIndex] = useState<number>(0);

  useEffect(() => {
    fetch("/api/get_all_folder_names")
      .then((response) => response.json())
      .then((responseData) => setFolderNames(responseData))
      .catch((error) => console.error("Error fetching data", error));
  }, [file]);

  useEffect(() => {
    if (selectedFolder) {
      fetch(`/api/get_all_files_in_folder?folderName=${selectedFolder}`)
        .then((response) => response.json())
        .then((responseData) => setFileNames(responseData))
        .catch((error) => console.error("Error fetching data", error));
    }
  }, [selectedFolder]);

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

  const handleSelect = (folderName: string) => {
    setSelectedFolder(folderName);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(e.target.value);
  };

  const handleButtonClick = () => {
    setSavedUserName(username);
  };

  const handleGrade = (grade: number) => {
    setGrade(grade);
  };

  const handleIndex = (index: number) => {
    setIndex(index);
  };
  const handleGradeUpload = async () => {
    if (!fileNames) {
      throw new Error("File names note provided");
    }

    const response = await fetch(
      `/api/grade_image?fileName=${fileNames.data[index]}&user=${username}&grade=${grade}`
    );

    if (response.ok) {
      console.log("graded sucessfully");
    } else {
      console.log("FAILED");
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="w-full flex-col max-w-5xl items-center justify-between font-mono text-sm lg:flex border-2 border-black p-2">
        <div>
          <input type="text" value={username} onChange={handleInputChange} />
          <button
            className="bg-gray-300 rounded-sm hover:bg-blue-300"
            onClick={handleButtonClick}
          >
            save
          </button>
          <p>username: {savedUserName}</p>
        </div>
        <div className="w-full">
          <h5 className="font-bold">Upload zipfile</h5>
          <input type="file" name="testimage" onChange={uploadToClient} />
          <button
            className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
            type="submit"
            onClick={uploadToServer}
          >
            send to server
          </button>
        </div>
        <hr className="w-full h-1 bg-blue-500 border-1 rounded m-2" />
        <div className="w-full">
          <div className="flex flex-row gap-x-2">
            <h4 className="font-bold">Selected Folder:</h4>
            {selectedFolder ? (
              <p>{selectedFolder}</p>
            ) : (
              <p>No folder selected</p>
            )}
          </div>
          {folderNames ? (
            <DropDown folderNames={folderNames.data} onSelect={handleSelect} />
          ) : (
            <p>loading...</p>
          )}
        </div>
        <hr className="w-full h-1 bg-blue-500 border-1 rounded m-2" />
        <div className="w-full">
          <div>
            <h5 className="font-bold">Files in DB:</h5>
            <div className="flex flex-row gap-x-3">
              <ul className="list-disc list-inside">
                {fileNames ? (
                  <ImageViewer
                    onImageIndex={handleIndex}
                    fileNames={fileNames.data}
                  />
                ) : (
                  <p>Loading...</p>
                )}
              </ul>
              <div>
                {fileNames ? (
                  <div className="flex flex-col gap-y-2 justify-center items-center">
                    <button
                      onClick={() => handleGrade(1)}
                      className="bg-green-400 hover:bg-green-500 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow"
                    >
                      class 1
                    </button>
                    <button
                      onClick={() => handleGrade(2)}
                      className="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow"
                    >
                      class 2
                    </button>
                    <button
                      onClick={() => handleGrade(3)}
                      className="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow"
                    >
                      class 3
                    </button>
                    <button
                      onClick={() => handleGrade(4)}
                      className="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow"
                    >
                      class 4
                    </button>
                    <button
                      onClick={() => handleGrade(5)}
                      className="bg-red-400 hover:bg-red-500 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow"
                    >
                      class 5
                    </button>
                  </div>
                ) : null}{" "}
              </div>
              <div className="flex flex-row gap-x-2">
                <p>Grade:</p>
                {grade ? <p>{grade}</p> : null}
              </div>
            </div>
            <button
              onClick={handleGradeUpload}
              className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow"
            >
              Upload grade
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}

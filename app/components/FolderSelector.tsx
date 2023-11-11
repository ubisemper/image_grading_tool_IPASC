import { useState, useEffect } from "react";
import DropDown from "@/app/components/DropDown";

interface FolderSelectorProps {
  onSelect: (folderName: string) => void;
  folderNames: returnData | null;
}

type returnData = {
  data: string[];
  message: string;
};

const FolderSelector = ({ onSelect, folderNames }: FolderSelectorProps) => {
  const [selectedFolder, setSelectedFolder] = useState("");

  const handleSelect = (folderName: string) => {
    setSelectedFolder(folderName);
    onSelect(folderName);
  };

  return (
    <div className="flex flex-col w-full p-4 bg-white rounded-lg shadow">
      {folderNames ? (
        <DropDown folderNames={folderNames.data} onSelect={handleSelect} />
      ) : (
        <p className="text-gray-400">loading...</p>
      )}
    </div>
  );
};

export default FolderSelector;

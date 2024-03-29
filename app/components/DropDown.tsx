import { Fragment, useState } from "react";
import { Menu, Transition } from "@headlessui/react";

type Props = {
  folderNames: string[];
  onSelect: (selectedFolder: string) => void;
};
const DropDown = ({ folderNames, onSelect }: Props) => {
  const [selectedFolder, setSelectedFolder] = useState("");
  const handleSelect = (folderName: string) => {
    setSelectedFolder(folderName);
    onSelect(folderName); // Call the onSelect callback with the selected folder
  };

  return (
    <Menu>
      <Menu.Button className="hover:bg-slate-400 p-2 rounded-md mb-2">
        Select dataset
      </Menu.Button>
      <Transition
        enter="transition duration-100 ease-out"
        enterFrom="transform scale-95 opacity-0"
        enterTo="transform scale-100 opacity-100"
        leave="transition duration-75 ease-out"
        leaveFrom="transform scale-100 opacity-100"
        leaveTo="transform scale-95 opacity-0"
      >
        <Menu.Items className="flex flex-col">
          {folderNames.map((folderName) => (
            /* Use the `active` state to conditionally style the active item. */
            <Menu.Item key={folderName} as={Fragment}>
              {({ active }) => (
                <p
                  className={`pl-2 truncate ${
                    active
                      ? "bg-blue-500 text-white rounded-md cursor-pointer"
                      : "bg-white text-black"
                  }`}
                  onClick={() => handleSelect(folderName)}
                >
                  {folderName}
                </p>
              )}
            </Menu.Item>
          ))}
        </Menu.Items>
      </Transition>
    </Menu>
  );
};

export default DropDown;

import React from "react";
import Image from "next/image";

const ImageComponent = ({ filename }: { filename: string }) => {
  const imageUrl = `/api/get_file_by_name?filename=${filename}`;

  return <Image src={imageUrl} alt="img" width={650} height={650} />;
};

export default ImageComponent;

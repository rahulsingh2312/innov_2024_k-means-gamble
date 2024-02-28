'use client'
import React, { useState } from 'react';
import { FaInstagram } from "react-icons/fa6";
import { CgMail } from "react-icons/cg";
import { FaFacebook } from "react-icons/fa6";
import axios from 'axios';

const BrochureGenerator = () => {
  const [product, setProduct] = useState('');
  const [brochure, setBrochure] = useState(null);
  const [location, setLocation] = useState(null);
  const [image, setImage] = useState('');
  const [caption, setCaption] = useState('');

  const handleGenerateBrochure = async () => {
    try {
      const response = await axios.post('http://localhost:5000/generate/brochure', {
        product,
        income_tier: 'High Spending,Low Income'
      });
      const data = response.data;
      setBrochure(data);
      const Captionresponse = await axios.post('http://localhost:5000/generate/caption', {
        product
      });
      console.log(Captionresponse)
      const Captiondata = Captionresponse.data;
      console.log(Captiondata);
      setCaption(Captiondata);
      console.log(caption);
      // Request image generation
      const imageResponse = await axios.post('http://localhost:5000/generate/image', {
        text: product
      });
      const imageData = imageResponse.data;
      setImage(imageData.image);

      const locationResponse = await axios.post('http://localhost:5000/locations', {
        product
      });
      console.log(locationResponse);
      const locationData = locationResponse.data;
      console.log(locationData);
      setLocation(locationData);


    } catch (error) {
      console.error('Error generating brochure or image or caption:', error);
    }
  };

  return (
<div className="flex flex-col items-center w-full">
      <div className='flex flex-col items-center bg-slate-200 rounded-lg w-96 p-4 my-4'>
        <h1 className="mt-4"> <strong>Title: High Income, High Spending</strong></h1>
        <label className='my-2'>
          Product:
          <input
            className='m-1 p-1 border-2 rounded-md'
            type="text"
            value={product}
            onChange={(e) => setProduct(e.target.value)}
          />
        </label>
        <button className='bg-green-500 mb-4 rounded-lg p-2 hover:bg-green-300 mx-auto' onClick={handleGenerateBrochure}>Generate Brochure Details</button>
      </div>

      <div className="flex mx-20 justify-center space-x-4">
        {brochure && (
          <div className="brochure-card w-1/3 bg-gray-100 rounded-lg p-4">
            <h2 className='text-center mb-4 font-bold'>Tagline:</h2>
            <p className='text-center mb-4'>{brochure.tagline}</p>
            <h2 className='text-center mb-4 font-bold'>Description:</h2>
            <p className='text-center'>{brochure.description}</p>
          </div>
        )}

        {image && (
          <div className="image-card w-1/3 bg-gray-100 rounded-lg p-4">
            <img className='mx-auto mb-4 w-80 rounded-md' src={`data:image/png;base64,${image}`} alt="Generated Image" />
          </div>
        )}

        {caption && (
          <div className="caption-card w-1/3 bg-gray-100 rounded-lg p-4">
            <h2 className='text-center mb-4 font-bold'>Social Media Caption:</h2>
            <div className="caption-content">
              <h3 className="text-center mb-2"><FaFacebook /></h3>
              <p className="text-center mb-2">{caption.facebook_caption}</p>
              <h3 className="text-center mb-2"><FaInstagram /></h3>
              <p className="text-center mb-2">{caption.insta_caption}</p>
              <h3 className="text-center mb-2"><CgMail /></h3>
              <p className="text-center">{caption.gmail_caption}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BrochureGenerator;

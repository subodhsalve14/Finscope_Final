import React from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

const FeatureCard = ({ title, description, tech, icon, link }) => {
  return (
    <Link to={link} className="block w-full h-full">
      <Card className="w-full transform transition-transform duration-300 hover:scale-105 hover:shadow-xl cursor-pointer h-full">
        <CardHeader>
          <CardTitle className="flex items-center text-xl font-bold">
            <span className="mr-2 text-2xl">{icon}</span>
            {title}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 mb-4">{description}</p>
          <div>
            <h4 className="font-semibold text-gray-800">ML/Tech Used:</h4>
            <p className="text-sm text-gray-600">{tech}</p>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
};

export default FeatureCard;

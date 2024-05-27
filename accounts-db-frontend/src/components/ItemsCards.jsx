import React from "react";
import SingleItemCard from "./SingleItemCard";

const ItemsCards = ({ itemsData }) => {
  return itemsData.map((item,i) => (
    <SingleItemCard
    index={i}
      category={item.category}
      key={item.mock_id}
      thumbnail_url={item.thumbnail_url}
      sub_category={item.sub_category}
      release_date={item.release_date}
      price={item.price}
      name={item.name}
      currency={item.currency}
      availability={!item.hidden}
    />
  ));
};

export default ItemsCards;

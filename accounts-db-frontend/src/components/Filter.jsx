import React, {useState} from "react";
import { motion } from "framer-motion";
const Filter = ({
  accountDetails,
  setSelectedCategory,
  setSelectedSubCategory,
  setSelectedCurrency,
  setSelectedAvailability,
  selectedCategory,
}) => {
  const [showSubCategory, setShowSubCategory] = useState(false);
  const [subCategories, setSubCategories] = useState([]);

  const handleCategoryChange = (event) => {
    setSelectedCategory(event.target.value);
    setShowSubCategory(!!event.target.value)
    accountDetails.categoriesData.map(function (value){
      if (value.name === event.target.value)
        setSubCategories(value['sub_categories'])
    })
  };

  const handleSubCategoryChange = (event) => {
    setSelectedSubCategory(event.target.value);
  };

  const handleCurrencyChange = (event) => {
    setSelectedCurrency(event.target.value);
  };
  const handleAvailabilityChange = (event) => {
    setSelectedAvailability(event.target.value);
  };

  return (
    <div className="order my-3">
      <div className="">
        <motion.label
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.2 }}
          htmlFor="category"
          className="form-label main-text-color"
        >
          Category:
        </motion.label>
        <motion.select
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.3, delay: 0.4 }}
          id="category"
          className="w-100"
          value={selectedCategory}
          onChange={handleCategoryChange}
        >
          <option value="" selected>
            -- choose category from the list --
          </option>
          {accountDetails.categoriesData.map((category) => (
            <option key={category.name} value={category.name}>
              {category.name}
            </option>
          ))}
        </motion.select>
        <motion.label
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.3, delay: 0.6 }}
          htmlFor="sub_category"
          hidden={!showSubCategory}
          className="form-label main-text-color pt-3"

        >
          Sub Category:
        </motion.label>
        <motion.select
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.3, delay: 0.8 }}
          id="sub_category"
          className="w-100"
          hidden={!showSubCategory}
          onChange={handleSubCategoryChange}
        >
          <option value="" selected>
            -- choose sub category from the list --
          </option>
          {
            subCategories.map((subCategory) => (
                <option key={subCategory} value={subCategory}>{subCategory.replaceAll('_', ' ')}</option>
            ))
          }

        </motion.select>
        <motion.label
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.3, delay: 0.8 }}
          htmlFor="currency"
          className="form-label main-text-color mt-3"
        >
          Currency:
        </motion.label>
        <motion.select
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.3, delay: 1 }}
          id="currency"
          className="w-100"
          onChange={handleCurrencyChange}
        >
          <option value="" selected>
            -- choose Currency from the list --
          </option>
          {["Coins", "Crowns", "Free", "Gems"].map((currency) => (
            <option key={currency} value={currency}>
              {currency}
            </option>
          ))}
        </motion.select>
        <motion.label
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.3, delay: 1.2 }}
          htmlFor="availability"
          className="form-label main-text-color mt-3"
        >
          Availability:
        </motion.label>
        <motion.select
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.3, delay: 1.4 }}
          id="availability"
          className="w-100"
          onChange={handleAvailabilityChange}
        >
          <option value="" selected>
            -- choose Availability from the list --
          </option>
          {[true, false].map((availability) => (
            <option key={availability} value={availability}>
              {availability ? "Available" : "Hidden"}
            </option>
          ))}
        </motion.select>
      </div>
    </div>
  );
};

export default Filter;

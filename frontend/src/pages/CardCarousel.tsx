import React from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";

export default function CardCarousel() {
  const cards = Array.from({ length: 10 }, (_, i) => ({
    title: `Card ${i + 1}`,
    content: `This is card ${i + 1}`,
  }));

  return (
    <div className="flex items-center gap-6 p-6">
      <div className="w-64 flex-none bg-gray-200 p-4 rounded-xl flex-shrink-0">
          <h2 className="text-xl font-bold">Left Content</h2>
          <p className="text-gray-600">This section stays fixed on the left.</p>
      </div>
      <div className="flex-1 overflow-hidden">
        <Swiper
          modules={[Navigation, Pagination]}
          spaceBetween={20}
          slidesPerView={4}
          navigation
          pagination={{ clickable: true }}
          loop={false}
          breakpoints={{
            320: { slidesPerView: 1 },  // Mobile
            640: { slidesPerView: 2 },  // Tablet
            1024: { slidesPerView: 4 }, // Desktop
          }}
          className="pb-10"
        >
          {cards.map((card, index) => (
            <SwiperSlide key={index}>
              <div className="bg-white rounded-2xl shadow-lg p-6 text-center">
                <h2 className="text-lg font-bold">{card.title}</h2>
                <p className="text-gray-600">{card.content}</p>
              </div>
            </SwiperSlide>
          ))}
        </Swiper>
      </div>
    </div>
  );
}

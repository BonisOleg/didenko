"""Seed HTML bodies for CMS pages (editable via admin TinyMCE).

Метрики «Про мене» — окреме поле Page.metrics (не в цьому HTML).
"""

ABOUT_BODY = """
<div class="about-lead" data-reveal>
  <p>Супроводжую клієнтів на всіх етапах процедури неплатоспроможності — від первинної консультації до прийняття остаточного рішення суду про повне списання боргів. Працюю професійно, конфіденційно та виключно в межах законодавства України.</p>
  <p>Моя мета — допомогти кожному, хто опинився у складній фінансовій ситуації, пройти процедуру банкрутства без зайвого стресу та отримати можливість почати фінансове життя з чистого аркуша.</p>
</div>

<section class="about-block" id="history" data-reveal aria-labelledby="about-history-title">
  <h2 id="about-history-title">Історія</h2>
  <p>Практика зосереджена на законному супроводі фізичних осіб у процедурах неплатоспроможності відповідно до Кодексу України з процедур банкрутства. Кожна справа починається з чесної оцінки перспектив і чіткого плану дій.</p>
  <p>Від першої консультації до фінального судового рішення клієнт отримує зрозумілий супровід: підготовку документів, взаємодію з судом і кредиторами, контроль етапів і захист конфіденційності.</p>
</section>

<section class="about-block" id="principles" data-reveal aria-labelledby="about-principles-title">
  <h2 id="about-principles-title">Принципи діяльності</h2>
  <p>Основа роботи — законність, захист даних клієнта та індивідуальний правовий шлях для кожної справи.</p>
  <div class="about-principles__grid">
    <article class="about-principle">
      <span class="about-principle__num">01</span>
      <h3>Законність та суворий регламент</h3>
      <p>Робота виключно в межах Кодексу України з процедур банкрутства.</p>
    </article>
    <article class="about-principle">
      <span class="about-principle__num">02</span>
      <h3>Конфіденційність</h3>
      <p>Повний захист персональних та фінансових даних клієнта.</p>
    </article>
    <article class="about-principle">
      <span class="about-principle__num">03</span>
      <h3>Індивідуальний підхід</h3>
      <p>Глибокий аналіз кожної справи та пошук оптимального правового шляху.</p>
    </article>
  </div>
</section>

<section class="about-block" id="team" data-reveal aria-labelledby="about-team-title">
  <h2 id="about-team-title">Команда</h2>
  <p>Практика побудована навколо персонального супроводу: клієнт завжди розуміє етап справи, наступний крок і правові ризики.</p>
  <div class="about-gallery" data-lightbox-group="team" aria-label="Фото команди">
    <figure>
      <img src="/static/img/about/team-1.jpg" alt="Робоча зустріч щодо підготовки документів" width="960" height="540" loading="lazy" decoding="async">
      <figcaption>Консультація та планування процедури</figcaption>
    </figure>
    <figure>
      <img src="/static/img/about/team-2.jpg" alt="Аналіз матеріалів справи" width="960" height="540" loading="lazy" decoding="async">
      <figcaption>Робота з матеріалами справи</figcaption>
    </figure>
  </div>
</section>

<section class="about-block" id="certificates" data-reveal aria-labelledby="about-certs-title">
  <h2 id="about-certs-title">Сертифікати та кваліфікація</h2>
  <p>Кваліфікація та правовий статус підтверджуються відповідністю вимогам законодавства щодо діяльності арбітражного керуючого.</p>
  <div class="about-certs">
    <article class="about-cert">
      <span class="about-cert__icon" aria-hidden="true">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
          <path d="M12 3 4.5 6.5v5.2c0 4.5 3.2 7.8 7.5 9.3 4.3-1.5 7.5-4.8 7.5-9.3V6.5L12 3Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>
          <path d="M9.2 12.2 11 14l3.8-3.8" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </span>
      <div>
        <h3>Правова кваліфікація</h3>
        <p>Діяльність арбітражного керуючого відповідно до норм чинного законодавства України.</p>
      </div>
    </article>
    <article class="about-cert">
      <span class="about-cert__icon" aria-hidden="true">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
          <path d="M7 3.5h7.2L19 8.3V20a1.5 1.5 0 0 1-1.5 1.5H7A1.5 1.5 0 0 1 5.5 20V5A1.5 1.5 0 0 1 7 3.5Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>
          <path d="M14 3.5V8h4.8" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>
          <path d="M8.5 12.5h7M8.5 16h5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>
        </svg>
      </span>
      <div>
        <h3>Процедурний супровід</h3>
        <p>Повний цикл документів і процесуальних дій у справах про неплатоспроможність фізичних осіб.</p>
      </div>
    </article>
  </div>
  <div class="about-gallery about-gallery--after" data-lightbox-group="docs" aria-label="Документи та матеріали">
    <figure>
      <img src="/static/img/about/docs-1.jpg" alt="Підготовка комплекту документів до суду" width="960" height="540" loading="lazy" decoding="async">
      <figcaption>Підготовка документів до суду</figcaption>
    </figure>
    <figure>
      <img src="/static/img/about/docs-2.jpg" alt="Правові матеріали та судова практика" width="960" height="540" loading="lazy" decoding="async">
      <figcaption>Судова практика та правові матеріали</figcaption>
    </figure>
    <figure>
      <img src="/static/img/about/docs-3.jpg" alt="Захист майна боржника" width="960" height="540" loading="lazy" decoding="async">
      <figcaption>Супровід щодо захисту майна</figcaption>
    </figure>
  </div>
</section>
""".strip()

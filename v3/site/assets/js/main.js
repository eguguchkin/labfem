(function(){
  "use strict";
  var TRAININGS = {
    persephona:{
      title:"Персефона", tag:"дочь, мать и своё царство",
      about:"Цикл о отделении, границах и праве на собственный сезон жизни. Мы читаем миф о спуске и возвращении, спорим с ним и переписываем его в личную сказку — ту, в которой у героини есть своё царство, а не только чужие ожидания.",
      prog:["Миф о Персефоне: чтение и переписывание сюжета спуска","Границы и отделение: где заканчивается мамина история","Тень и сезонность: право на свою зиму и свою весну","Образ дочери и образ матери: диалог двух ролей","Возвращение: свой сад, свои плоды"],
      meta:"8 встреч · раз в неделю · 3 часа · группа до 10 участниц · усадьба «Гуслица»",
      site:"https://example.org/cycles/persephona", topic:"persephona"
    },
    venus:{
      title:"Венера", tag:"тело, желание, красота",
      about:"Цикл о телесности, либидо и красоте: возвращаем себе право на удовольствие, видимость и любовь к собственному телу. Смотрим на Венеру от палеолита до Боттичелли — и ищем свой образ, а не чужой взгляд.",
      prog:["Тело в искусстве: Венера от палеолита до Боттичелли","Зеркало и взгляд: чьими глазами мы видим себя","Желание и либидо: карта собственной силы","Живопись тела: отпечатки, контуры, цвет","Интенсив на террасе: движение и видимость"],
      meta:"6 встреч + осенний интенсив на террасе · группа до 10 участниц · Москва",
      site:"https://example.org/cycles/venus", topic:"venus"
    },
    demeter:{
      title:"Деметра", tag:"забота и её пределы",
      about:"Цикл для тех, кто заботится: матери, дочери, помогающие. Учимся отличать заботу от истощения, проводить границу урожая и цены остановки, находить собственные источники силы — сад, стол, тишину.",
      prog:["Миф о Деметре: забота, урожай и цена остановки","Источники и истощение: бережная инвентаризация сил","Материнские сценарии: что берём, что оставляем","Забота о себе без вины: практика малых ритуалов","Ритуалы восстановления: сад, стол, тишина"],
      meta:"5 встреч · суббота раз в две недели · 3,5 часа · усадьба «Гуслица»",
      site:"https://example.org/cycles/demeter", topic:"demeter"
    },
    ariadne:{
      title:"Ариадна", tag:"нить и призвание",
      about:"Цикл о призвании и собственном маршруте: из чего ткётся наша нить, как не потерять её в чужом лабиринте и кто наши свидетели на выходе. Много визуальных практик и работы с образом проекта-жизни.",
      prog:["Миф об Ариадне: нить, лабиринт и брошенность","Призвание против маршрута: свой темп и своя дорога","Ткачество проекта: из чего сделана моя нить","Лабиринт и его свидетели: поддержка вместо спасения","Выход из лабиринта: ритуал завершения"],
      meta:"7 встреч · вечерний формат · 3 часа · пространство «Кристалл», Москва",
      site:"https://example.org/cycles/ariadne", topic:"ariadne"
    }
  };

  /* reveal on scroll */
  var io = new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('on'); io.unobserve(e.target); } });
  },{threshold:.12});
  document.querySelectorAll('.rv').forEach(function(el){ io.observe(el); });

  /* active nav */
  var navLinks = document.querySelectorAll('.links a[data-sec]');
  var secIO = new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(e.isIntersecting){
        navLinks.forEach(function(a){ a.classList.toggle('active', a.dataset.sec === e.target.id); });
      }
    });
  },{rootMargin:'-42% 0px -52% 0px'});
  ['s1','s2','s3','s4','s5','s6','s7','s8'].forEach(function(id){
    var el = document.getElementById(id); if(el) secIO.observe(el);
  });

  /* burger */
  var burger = document.getElementById('burger');
  burger.addEventListener('click', function(){
    var open = document.body.classList.toggle('menu');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.querySelectorAll('.overlay a.ov').forEach(function(a){
    a.addEventListener('click', function(){
      document.body.classList.remove('menu');
      burger.setAttribute('aria-expanded','false');
    });
  });

  /* modal */
  var modal = document.getElementById('modal'),
      mTitle = document.getElementById('mTitle'), mTag = document.getElementById('mTag'),
      mAbout = document.getElementById('mAbout'), mProg = document.getElementById('mProg'),
      mMeta = document.getElementById('mMeta'), mSite = document.getElementById('mSite'),
      mJoin = document.getElementById('mJoin'), current = null;
  function openModal(slug){
    var t = TRAININGS[slug]; if(!t) return;
    current = slug;
    mTitle.textContent = t.title;
    mTag.textContent = t.tag;
    mAbout.textContent = t.about;
    mProg.replaceChildren.apply(mProg, t.prog.map(function(p){
      var li = document.createElement('li'); li.textContent = p; return li;
    }));
    mMeta.textContent = t.meta;
    mSite.href = t.site;
    modal.hidden = false;
    document.body.classList.add('modal-open');
  }
  function closeModal(){
    modal.hidden = true;
    document.body.classList.remove('modal-open');
  }
  document.querySelectorAll('[data-training]').forEach(function(b){
    b.addEventListener('click', function(){ openModal(b.dataset.training); });
  });
  modal.addEventListener('click', function(e){ if(e.target.hasAttribute('data-close')) closeModal(); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && !modal.hidden) closeModal(); });
  mJoin.addEventListener('click', function(){
    var t = TRAININGS[current]; if(!t) return;
    closeModal();
    var sel = document.getElementById('fTopic');
    sel.value = t.topic;
    var card = document.getElementById('inviteForm');
    card.classList.add('flash');
    setTimeout(function(){ card.classList.remove('flash'); }, 1600);
    document.getElementById('s8').scrollIntoView({behavior:'smooth'});
    setTimeout(function(){ document.getElementById('fName').focus({preventScroll:true}); }, 700);
  });

  /* form */
  var form = document.getElementById('inviteForm'),
      msg = document.getElementById('formMsg');
  form.addEventListener('submit', function(e){
    e.preventDefault();
    var email = document.getElementById('fEmail').value.trim(),
        name = document.getElementById('fName').value.trim();
    if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)){
      msg.className = 'form-msg err';
      msg.textContent = 'Проверьте почту: кажется, в адресе не хватает буквы или точки.';
      return;
    }
    msg.className = 'form-msg ok';
    msg.textContent = 'Спасибо' + (name ? ', ' + name : '') + '! Письмо уже в пути: ответим на ' + email + ' в течение двух дней.';
    form.reset();
  });

  /* totop + parallax */
  var totop = document.getElementById('totop'),
      heroFig = document.getElementById('heroFig'),
      reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches,
      tick = false;
  function onScroll(){
    var y = window.scrollY || 0;
    totop.classList.toggle('show', y > 600);
    if(!reduce && heroFig && y < window.innerHeight * 1.2){
      heroFig.style.transform = 'translate3d(0,' + (y * 0.05).toFixed(1) + 'px,0)';
    }
    tick = false;
  }
  window.addEventListener('scroll', function(){
    if(!tick){ tick = true; requestAnimationFrame(onScroll); }
  }, {passive:true});
  totop.addEventListener('click', function(){ window.scrollTo({top:0, behavior:'smooth'}); });

  document.getElementById('year').textContent = new Date().getFullYear();
  onScroll();
})();

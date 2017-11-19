//@jdnichollsc - Creator of this PoC
//@rapitors - Collaborator

var game = new Phaser.Game(1024, 768, Phaser.AUTO, '', {
  init: function(){
    this.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;
    this.scale.maxWidth = 1024;
    this.scale.maxHeight = 768;
    this.scale.pageAlignHorizontally = true;
    this.scale.pageAlignVertically = true;
    this.scale.updateLayout();
  },
  preload: function(){
    this.game.load.image('race', raceURI);
    this.game.load.image('car', carURI);
    this.game.load.image('zoomIn', zoomInURI);
    this.game.load.image('zoomOut', zoomOutURI);
  },
  render: function(){
    if(this.game.world.scale.x == 1) {
      this.game.debug.box2dWorld();
    }
  },
  create: function(){

    this.box2dPlugin = this.game.add.text(this.game.width/2 - 300, this.game.height/2 + 80, "Hecho con el Plugin Box2D!\n@jdnichollsc - @rapitors",
    {
      font: 'bold 60px Arial',
      fill: "#FFF"
    });
   this.box2dPlugin.addFontWeight('normal', 0);      this.box2dPlugin.addFontWeight('bold', 20);

    this.points = GAME_DATA.points
    this.leftPoints = { x: [], y: [] };
    this.rightPoints = { x: [], y: [] };

    this.tweenData = this.generateData(this.points);
    this.graphics = this.game.add.graphics(0, 0);

    this.race = this.game.cache.getFrame('race');

    this.createPath();
    this.createSidePoints();
    this.tweenDataLeft = this.generateData(this.leftPoints);
    this.tweenDataRight = this.generateData(this.rightPoints);

    var leftPoints = this.dataToChain(this.tweenDataLeft);
    var middlePoints = this.dataToChain(this.tweenData);
    var rightPoints = this.dataToChain(this.tweenDataRight);

    this.game.world.setBounds(0, 0, 2600, 2600);
    this.game.physics.startSystem(Phaser.Physics.BOX2D);
    this.game.physics.box2d.setBoundsToWorld();
    this.game.physics.box2d.density = 1;
    this.game.physics.box2d.friction = 0.3;
    this.game.physics.box2d.restitution = 0.2;


    this.roadLeft = new Phaser.Physics.Box2D.Body(this.game, null, 0, 0, 0);
	  this.roadLeft.setChain(leftPoints);

    this.roadRight = new Phaser.Physics.Box2D.Body(this.game, null, 0, 0, 0);
	  this.roadRight.setChain(rightPoints);

    this.cursors = this.game.input.keyboard.createCursorKeys();

    this.car = this.game.add.sprite(this.tweenData[0].x, this.tweenData[0].y, 'car');
    this.game.physics.box2d.enable(this.car);
    this.camera.follow(this.car);
    this.car.body.setRectangle(70, 28);

    this.zoom = this.game.add.button(0, this.game.height, 'zoomIn', this.changeZoom, this);
    this.zoom.inputEnabled = true;
    this.zoom.input.useHandCursor = true;
    this.zoom.anchor.y = 1;
    this.zoom.fixedToCamera = true;
  },
  changeZoom: function(){
    var newZoom = this.game.world.scale.x == 1 ? 2 : 1;
    this.game.world.scale.set(newZoom);
    if(newZoom == 1){
      this.zoom.loadTexture("zoomIn");
      this.zoom.scale.set(1);
      this.graphics.visible = true;
    }else{
      this.zoom.loadTexture("zoomOut");
      this.zoom.scale.set(0.5);
      this.graphics.visible = false;
    }
  },
  controlCar: function(){
    this.car.body.setZeroVelocity();
    if (this.cursors.left.isDown) {
        this.car.body.rotateLeft(200);
    }
    else if (this.cursors.right.isDown) {
        this.car.body.rotateRight(200);
    }
    else {
        this.car.body.setZeroRotation();
    }

    if (this.cursors.up.isDown) {
     this.car.body.velocity.x = (Math.cos(this.game.math.degToRad(this.car.angle)) * 300);
     this.car.body.velocity.y =(Math.sin(this.game.math.degToRad(this.car.angle)) * 300);
    } else if (this.cursors.down.isDown) {
      this.car.body.velocity.x = - (Math.cos(this.game.math.degToRad(this.car.angle)) * 300);
      this.car.body.velocity.y = -(Math.sin(this.game.math.degToRad(this.car.angle)) * 300);
    }
  },
  generateData: function(points){
    var firstPoint = new Phaser.Point(points.x[0], points.y[0]);
    points.x.shift();
    points.y.shift();

    var data = this.game.add.tween({ x: firstPoint.x, y: firstPoint.y }).to( { x: points.x, y: points.y }, 8000, "Linear", true).interpolation(function(v, k){
      return Phaser.Math.catmullRomInterpolation(v, k);
    }).generateData(60);

    points.x.unshift(firstPoint.x);
    points.y.unshift(firstPoint.y);
    return data;
  },
  createPath: function(){

    var tracks = this.tweenData.length / this.race.width;
    this.game.add.rope(this.tweenData[0].x, this.tweenData[0].y, 'race', null, this.createRopePoints(0));

    for(var i = 1; i < tracks; i++){
      var pos = i * this.race.width;

      this.game.add.rope(this.tweenData[pos].x, this.tweenData[pos].y, 'race', null, this.createRopePoints(pos));
    }
  },
  createSidePoints: function(){
    this.game.world.bringToTop(this.graphics);
    this.drawCircle(this.points.x[0], this.points.y[0], 0xFF0000, 18);
    var index = this.findIndexPointInGeneratedData({ x: this.points.x[0], y: this.points.y[0]});

      this.drawEndPoints(index, 1);

    for(var i = 1; i < this.points.x.length;i++){

      this.drawCircle(this.points.x[i], this.points.y[i], 0xFF0000, 18);

      var index = this.findIndexPointInGeneratedData({ x: this.points.x[i], y: this.points.y[i]});

      this.drawEndPoints(index, -1);
    }
  },
  drawEndPoints: function(index, direction){
    var indexA, indexB;
    if(direction > 0){
      indexA = index + 1;
      indexB = index;
    }
    else{
      indexA = index - 1;
      indexB = index;
    }
    var A = new Phaser.Point(this.tweenData[indexA].x, this.tweenData[indexA].y);
    var B = new Phaser.Point(this.tweenData[indexB].x, this.tweenData[indexB].y);

    var C = new Phaser.Point();
    var D = new Phaser.Point();
    this.findSidePoints(A, B, this.race.height/2, C, D);
    this.drawCircle(C.x, C.y, 0x0000FF, 18);
    this.drawCircle(D.x, D.y, 0x00FF00, 18);
    this.leftPoints.x.push(C.x);
    this.leftPoints.y.push(C.y);
    this.rightPoints.x.push(D.x);
    this.rightPoints.y.push(D.y);
  },
  drawCircle: function(x, y, c, s){
    this.graphics.lineStyle(0);
    this.graphics.beginFill(c, 1);
    this.graphics.drawCircle(x, y, s);
    this.graphics.endFill();
  },
  createRopePoints : function(iniPos){
    var points = [];
    var finPos = iniPos + this.race.width;
    if(!this.tweenData[finPos]) finPos = this.tweenData.length - 1;

    var color = Phaser.Color.getRandomColor(100, 255);

    for(var i = iniPos; i<= finPos; i++){

      points.push(new Phaser.Point(this.tweenData[i].x - this.tweenData[iniPos].x, this.tweenData[i].y - this.tweenData[iniPos].y));

      this.drawCircle(this.tweenData[i].x, this.tweenData[i].y, color, 12);
    }
    return points;
  },
  update: function(){
    var x = Math.round(this.game.input.activePointer.position.x);
    var y = Math.round(this.game.input.activePointer.position.y);
    this.game.debug.text("x:" + x + " y:" + y, 20, 30);
    this.controlCar();
    //this.game.world.angle = this.car.angle - 90;
    //this.game.world.pivot.setTo(this.car.x - this.game.width/2, this.car.y - this.game.height/2);
//this.game.camera.focusOnXY(this.car.x, this.car.y);
  },
  dataToChain: function(data){
    var chain = [];
    for(var i = 0; i < data.length; i+= 10){
      chain.push(data[i].x);
      chain.push(data[i].y);
    }
    chain.push(data[data.length -1].x);
    chain.push(data[data.length -1].y)
    return chain;
  },
  findSidePoints: function(pointA, pointB, distance, leftPoint, rightPoint){

    var a = distance;
    var c = pointA.distance(pointB);
    var dx = (a * (pointA.y - pointB.y) / c);
    var dy = (a * (pointB.x - pointA.x) / c);
    rightPoint.x = pointB.x + dx;
    rightPoint.y = pointB.y + dy;
    leftPoint.x = pointB.x - dx;
    leftPoint.y = pointB.y - dy;
  },
  findIndexPointInGeneratedData: function(point){
    var index = 0;
    for(var i = 0; i < this.tweenData.length; i ++){
      if(Phaser.Point.distance(point, this.tweenData[i]) < 5){
        index = i;
        break;
      }
    }
    return index;
  }
});
